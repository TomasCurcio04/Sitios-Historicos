# pylint: disable=import-error
"""Servicio para manejo de visitas de sitios."""

from src.core.entity.site_visit import SiteVisit
from src.core.database import db


def add_site_visit(site_id):
    """Incrementa el contador de visitas de un sitio.

    Args:
        site_id: ID del sitio a incrementar
    """
    visit = db.session.query(SiteVisit).filter_by(id_site=site_id).first()
    if not visit:
        visit = SiteVisit(id_site=site_id, visit_count=1)
        db.session.add(visit)
    else:
        visit.visit_count += 1
    db.session.commit()
