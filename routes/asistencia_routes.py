from flask import Blueprint, render_template
from controllers.asistencia_controller import (
    buscar_por_dni, trabajador_de_usuario, registrar_asistencia, listar_asistencias,
    marcar_entrada, marcar_salida
)
from utils.decorators import login_required

asistencia_bp = Blueprint("asistencia", __name__)


@asistencia_bp.route("/asistencia", methods=["GET"])
@login_required
def vista_asistencia():
    return render_template("asistencia/index.html")


asistencia_bp.route("/api/asistencias/buscar/<dni>", methods=["GET"])(login_required(buscar_por_dni))
asistencia_bp.route("/api/asistencias/mi-trabajador", methods=["GET"])(login_required(trabajador_de_usuario))
asistencia_bp.route("/api/asistencias", methods=["POST"])(login_required(registrar_asistencia))
asistencia_bp.route("/api/asistencias", methods=["GET"])(login_required(listar_asistencias))
asistencia_bp.route("/api/asistencias/<int:id>/entrada", methods=["PUT"])(login_required(marcar_entrada))
asistencia_bp.route("/api/asistencias/<int:id>/salida", methods=["PUT"])(login_required(marcar_salida))
