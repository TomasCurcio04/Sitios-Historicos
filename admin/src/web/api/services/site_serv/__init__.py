"""Servicios de sitios para la API"""

from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload
from src.core.database import db
from src.core.entity.site import Site, site_tag
from src.core.entity.state import State
from src.core.entity.tag import Tag
from src.core.entity.review import Review
from src.core.entity.site_image import SiteImage
from src.core.services.board.site_views import add_site_visit


def listar_sitios(
    name=None,
    description=None,
    city=None,
    province=None,
    tags=None,
    order_by=None,
    lat=None,
    long=None,
    radius=None,
    page=1,
    per_page=20,
    conservation_state=None,
    search=None,
    user_id=None,
    search_favorites=False,
):
    """Listar sitios con filtros y paginación"""
    query = db.session.query(Site).filter(Site.is_visible, ~Site.deleted)

    # Si search_favorites es True y hay user_id, filtrar por favoritos
    if search_favorites and user_id:
        from src.core.entity.site_favorite import SiteFavorite

        query = query.join(SiteFavorite, Site.id_site == SiteFavorite.id_site)
        query = query.filter(SiteFavorite.id_public_user == user_id)

    # Join con state_rel y eager loading de relaciones
    query = query.join(State, Site.state == State.id_state)
    query = query.options(
        joinedload(Site.state_rel), joinedload(Site.tag), joinedload(Site.images)
    )

    # Filtro por nombre
    if name:
        query = query.filter(Site.name.ilike(f"%{name}%"))

    # Búsqueda general por texto (nombre y descripción breve)
    if search:
        query = query.filter(
            or_(
                Site.name.ilike(f"%{search}%"),
                Site.short_description.ilike(f"%{search}%"),
            )
        )

    # Filtro por descripción
    if description:
        query = query.filter(
            or_(
                Site.short_description.ilike(f"%{description}%"),
                Site.full_description.ilike(f"%{description}%"),
            )
        )

    # Filtro por ciudad
    if city:
        query = query.filter(Site.city.ilike(city))

    # Filtro por provincia
    if province:
        query = query.filter(State.name.ilike(province))

    # Filtro por estado de conservación
    if conservation_state:
        query = query.filter(Site.conservation_state.ilike(conservation_state))

    # Filtro por tags
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",")]
        query = query.join(site_tag).join(Tag).filter(Tag.name.in_(tag_list))

    # Filtro geoespacial
    if lat and long and radius:
        distance = func.sqrt(
            func.pow(111.1 * (Site.latitude - lat), 2)
            + func.pow(
                111.1 * (Site.longitude - long) * func.cos(Site.latitude / 57.3), 2
            )
        )
        query = query.filter(distance <= radius)

    # Ordenamiento
    if order_by == "latest":
        query = query.order_by(Site.date_registered.desc())
    elif order_by == "oldest":
        query = query.order_by(Site.date_registered.asc())
    elif order_by == "rating-5-1":
        # Ordenar por rating promedio descendente (5 a 1)
        avg_rating = (
            db.session.query(
                Review.id_site, func.avg(Review.rating).label("avg_rating")
            )
            .filter(Review.status == "APROBADA")
            .group_by(Review.id_site)
            .subquery()
        )

        query = query.outerjoin(avg_rating, Site.id_site == avg_rating.c.id_site)
        query = query.order_by(avg_rating.c.avg_rating.desc().nullslast())
    elif order_by == "rating-1-5":
        # Ordenar por rating promedio ascendente (1 a 5)
        avg_rating = (
            db.session.query(
                Review.id_site, func.avg(Review.rating).label("avg_rating")
            )
            .group_by(Review.id_site)
            .subquery()
        )

        query = query.outerjoin(avg_rating, Site.id_site == avg_rating.c.id_site)
        query = query.order_by(avg_rating.c.avg_rating.asc().nullsfirst())
    elif order_by == "name-asc":
        query = query.order_by(Site.name.asc())
    elif order_by == "name-desc":
        query = query.order_by(Site.name.desc())
    elif order_by == "most-visited":
        # Ordenar por visitas descendente
        from src.core.entity.site_visit import SiteVisit

        query = query.outerjoin(SiteVisit, Site.id_site == SiteVisit.id_site)
        query = query.order_by(SiteVisit.visit_count.desc().nullslast())
    else:
        query = query.order_by(Site.id_site)

    # Paginación
    total = query.count()
    items = query.offset((page - 1) * per_page).limit(per_page).all()

    return {"total": total, "page": page, "per_page": per_page, "items": items}


def get_site_by_id_service(site_id):
    """Obtiene un sitio por ID y registra la visita"""
    # Obtener sitio con relaciones
    site = (
        db.session.query(Site)
        .filter(Site.id_site == site_id, Site.is_visible, ~Site.deleted)
        .options(
            joinedload(Site.state_rel), joinedload(Site.tag), joinedload(Site.images)
        )
        .first()
    )

    if not site:
        return None

    # Registrar visita
    try:
        add_site_visit(site_id)
    except Exception:
        pass  # Si falla el registro de visita, no afecta la respuesta

    return site


def create_site_service(site_data, user_id):
    """Crea un nuevo sitio histórico en la base de datos"""
    from datetime import datetime, timezone

    # Buscar provincia por nombre
    state = (
        db.session.query(State).filter(State.name.ilike(site_data["province"])).first()
    )

    if not state:
        raise ValueError(f"Province '{site_data['province']}' not found")

    # Crear sitio (inicialmente no visible hasta aprobación)
    site = Site(
        name=site_data["name"],
        short_description=site_data["short_description"],
        full_description=site_data["description"],
        city=site_data["city"],
        state=state.id_state,
        latitude=site_data["lat"],
        longitude=site_data["long"],
        conservation_state=site_data["state_of_conservation"],
        category=1,  # Categoría por defecto
        created_by=user_id,
        is_visible=False,  # Requiere aprobación
        date_registered=datetime.now(timezone.utc),
    )

    db.session.add(site)
    db.session.flush()  # Para obtener el ID

    # Procesar tags
    for tag_name in site_data["tags"]:
        tag = db.session.query(Tag).filter(Tag.name.ilike(tag_name.strip())).first()

        if not tag:
            # Crear tag si no existe
            tag = Tag(name=tag_name.strip())
            db.session.add(tag)
            db.session.flush()

        site.tag.append(tag)

    db.session.commit()

    # Recargar con relaciones
    return (
        db.session.query(Site)
        .filter(Site.id_site == site.id_site)
        .options(
            joinedload(Site.state_rel), joinedload(Site.tag), joinedload(Site.images)
        )
        .first()
    )
