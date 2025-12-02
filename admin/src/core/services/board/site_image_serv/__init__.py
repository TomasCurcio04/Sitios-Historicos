"""Servicios básicos para manejo de imágenes de sitios."""

from src.core.database import db
from src.core.entity.site_image import SiteImage


def crear_imagen(**kwargs):
    """Crea una nueva imagen para un sitio."""
    imagen = SiteImage(**kwargs)
    db.session.add(imagen)
    return imagen


def obtener_imagenes_por_sitio(id_site, **kwargs):
    """Obtiene todas las imágenes de un sitio ordenadas por display_order."""
    query = db.session.query(SiteImage).filter_by(id_site=id_site)
    if kwargs:
        query = query.filter_by(**kwargs)
    return query.order_by(SiteImage.display_order).all()


def obtener_thumbnail(id_site, **kwargs):
    """Obtiene la imagen thumbnail de un sitio."""
    filtros = {"id_site": id_site, "is_thumbnail": True, **kwargs}
    return db.session.query(SiteImage).filter_by(**filtros).first()


def eliminar_imagen(id_imagen):
    """Elimina una imagen por su ID."""
    imagen = db.session.get(SiteImage, id_imagen)
    if imagen:
        db.session.delete(imagen)
    return imagen


def actualizar_imagen(id_imagen, **kwargs):
    """Actualiza una imagen con los datos proporcionados."""
    return db.session.query(SiteImage).filter_by(id_site_image=id_imagen).update(kwargs)


def actualizar_thumbnail(id_site, id_nueva_thumbnail):
    """Actualiza cuál imagen es el thumbnail de un sitio."""
    db.session.query(SiteImage).filter_by(id_site=id_site, is_thumbnail=True).update(
        {"is_thumbnail": False}
    )
    db.session.query(SiteImage).filter_by(id_site_image=id_nueva_thumbnail).update(
        {"is_thumbnail": True}
    )
