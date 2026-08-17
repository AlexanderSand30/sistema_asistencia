from flask import Blueprint, render_template, session, redirect, url_for
from controllers.asistencia_controller import (
    buscar_por_dni, registrar_asistencia, listar_asistencias,
    marcar_entrada, marcar_salida
)

asistencia_bp = Blueprint("asistencia", __name__)


@asistencia_bp.route("/asistencia", methods=["GET"])
def vista_asistencia():
    if not session.get("usuario_id"):
        return redirect(url_for("usuario.login"))
    return render_template("asistencia.html")


asistencia_bp.route("/api/asistencias/buscar/<dni>", methods=["GET"])(buscar_por_dni)
asistencia_bp.route("/api/asistencias", methods=["POST"])(registrar_asistencia)
asistencia_bp.route("/api/asistencias", methods=["GET"])(listar_asistencias)
asistencia_bp.route("/api/asistencias/<int:id>/entrada", methods=["PUT"])(marcar_entrada)
asistencia_bp.route("/api/asistencias/<int:id>/salida", methods=["PUT"])(marcar_salida)
