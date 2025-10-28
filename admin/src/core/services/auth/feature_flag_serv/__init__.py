# pylint: disable=import-error
"""Servicio de feature flags."""

from src.core.entity.feature_flag import FeatureFlag
from src.core.database import db


def list_feature_flags():
    """Lista todas las feature flags del sistema.
    
    Returns:
        Lista de feature flags ordenadas por ID
    """
    flags = db.session.query(FeatureFlag).order_by(FeatureFlag.id).all()
    return flags


def get_feature_flag(name):
    """Obtiene una feature flag por su nombre.
    
    Args:
        name: Nombre de la feature flag
    
    Returns:
        Feature flag encontrada o None
    """
    flag = db.session.query(FeatureFlag).filter_by(name=name).first()
    return flag


def modify_feature_flag(name, enabled, updated_by, maintenance_message=None):
    """Modifica una feature flag existente.
    
    Args:
        name: Nombre de la feature flag
        enabled: Estado activo/inactivo
        updated_by: ID del usuario que actualiza
        maintenance_message: Mensaje de mantenimiento (opcional)
    
    Returns:
        Feature flag modificada
    
    Raises:
        ValueError: Si el mensaje supera los 50 caracteres
    """
    flag = FeatureFlag.get_flag(name)
    if flag:
        flag.enabled = enabled
        flag.updated_by = updated_by
        if maintenance_message is not None:
            if len(maintenance_message) > 50:
                raise ValueError("El mensaje de mantenimiento no puede superar los 50 caracteres")
            flag.maintenance_message = maintenance_message
        db.session.commit()
    return flag


def get_feature_flag_fresh(name):
    """Obtiene una feature flag actualizada desde la base de datos.
    
    Args:
        name: Nombre de la feature flag
    
    Returns:
        Feature flag fresca desde la DB
    """
    db.session.expire_all()
    flag = db.session.query(FeatureFlag).filter_by(name=name).first()
    return flag


def update_feature_flags(flags_data, updated_by):
    """Actualiza múltiples feature flags en lote.
    
    Args:
        flags_data: Dict con datos de las flags a actualizar
        updated_by: ID del usuario que actualiza
    
    Returns:
        True si hubo cambios, False en caso contrario
    
    Raises:
        ValueError: Si algún mensaje supera los 50 caracteres
    """
    flags = list_feature_flags()
    has_changes = False
    for flag in flags:
        flag_id = str(flag.id)
        if flag_id in flags_data:
            new_enabled = flags_data[flag_id].get("enabled", False)
            new_message = flags_data[flag_id].get("maintenance_message", "")
            
            if new_message and len(new_message) > 50:
                raise ValueError(f"El mensaje de mantenimiento para '{flag.name}' no puede superar los 50 caracteres")

            if flag.enabled != new_enabled or flag.maintenance_message != new_message:
                flag.enabled = new_enabled
                flag.maintenance_message = new_message
                flag.updated_by = updated_by
                has_changes = True

    if has_changes:
        db.session.commit()
        db.session.expire_all()
    return has_changes