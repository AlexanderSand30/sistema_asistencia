from flask import Blueprint, render_template, session, redirect, url_for
from controllers.trabajador_controller import (
    listar_trabajadores, listar_inactivos, crear_trabajador,
    actualizar_trabajador, eliminar_trabajador, reactivar_trabajador
)

trabajador_bp = Blueprint("trabajador", __name__)


@trabajador_bp.route("/trabajadores", methods=["GET"])
def vista_trabajadores():
    if not session.get("usuario_id"):
        return redirect(url_for("usuario.login"))
    if session.get("rol") != "admin":
        return "No autorizado", 403
    return render_template("trabajadores/index.html")


trabajador_bp.route("/api/trabajadores", methods=["GET"])(listar_trabajadores)
trabajador_bp.route("/api/trabajadores/inactivos", methods=["GET"])(listar_inactivos)
trabajador_bp.route("/api/trabajadores", methods=["POST"])(crear_trabajador)
trabajador_bp.route("/api/trabajadores/<int:id>", methods=["PUT"])(actualizar_trabajador)
trabajador_bp.route("/api/trabajadores/<int:id>", methods=["DELETE"])(eliminar_trabajador)
trabajador_bp.route("/api/trabajadores/<int:id>/reactivar", methods=["PUT"])(reactivar_trabajador)