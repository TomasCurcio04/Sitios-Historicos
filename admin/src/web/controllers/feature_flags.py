"""Controlador de feature flags para configuración del sistema."""

from flask import request, render_template, redirect, url_for, flash, Blueprint, session
from src.web.handlers.utils import admin_maintenance_required
from src.core.services.auth.user_serv import buscar_usuario
from src.core.services.auth.feature_flag_serv import (
    list_feature_flags,
    update_feature_flags,
)

feature_flags_bp = Blueprint("feature_flags", __name__, url_prefix="/feature_flags")


@feature_flags_bp.route("/", methods=["GET", "POST"], endpoint="feature_flags")
@admin_maintenance_required
def feature_flags():
    """Gestiona la configuración de feature flags del sistema.

    GET:
        - Muestra el formulario de configuración con las flags actuales.
    POST:
        - Valida y actualiza las feature flags en base al formulario.

    Returns:
        Response: Plantilla renderizada (GET) o redirección tras el POST.
    """
    usuario = buscar_usuario(session["user"]["email"])
    usuario_id = usuario.id_user if usuario else 1

    if request.method == "POST":
        flags = list_feature_flags()
        flags_data = {}
        admin_maintenance_disabled = False
        for flag in flags:
            new_enabled = f"enabled_{flag.id}" in request.form
            new_message = request.form.get(f"mensaje_{flag.id}", "")

            # Validar admin_maintenance_mode
            if flag.name == "admin_maintenance_mode":
                if flag.enabled and not new_enabled:
                    admin_maintenance_disabled = True
                    new_message = ""  # Borrar mensaje al desactivar
                    # Limpiar mensajes flash existentes
                    session.pop("_flashes", None)
                elif not flag.enabled and new_enabled and not new_message.strip():
                    flash("El modo mantenimiento requiere un mensaje", "error")
                    return redirect(url_for("feature_flags.feature_flags"))

            flags_data[str(flag.id)] = {
                "enabled": new_enabled,
                "maintenance_message": new_message,
            }
        try:
            has_changes = update_feature_flags(flags_data, usuario_id)
            if has_changes:
                if admin_maintenance_disabled:
                    flash("Mantenimiento desactivado", "success")
                else:
                    flash("Feature flags actualizados correctamente", "success")
            else:
                flash("No se detectaron cambios", "info")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("feature_flags.feature_flags"))

    # Obtener flags frescos para GET
    flags = list_feature_flags()
    return render_template("feature_flags.html", flags=flags)
