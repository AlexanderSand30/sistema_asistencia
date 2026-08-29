from flask import Blueprint, render_template
from utils.decorators import login_required, admin_required
from controllers.trabajador_controller import (
    listar_trabajadores,
    listar_inactivos,
    crear_trabajador,
    mostrar_trabajador,
    actualizar_trabajador,
    eliminar_trabajador,
    reactivar_trabajador,
    search_trabajador
)

trabajador_bp = Blueprint("trabajador", __name__)


@trabajador_bp.route("/trabajadores", methods=["GET"])
@login_required
@admin_required
def vista_trabajadores():
    return render_template("trabajadores/index.html")


trabajador_bp.route("/api/trabajadores", methods=["GET"])(login_required(listar_trabajadores))
trabajador_bp.route("/api/trabajadores/inactivos", methods=["GET"])(login_required(listar_inactivos))
trabajador_bp.route("/api/trabajadores", methods=["POST"])(login_required(crear_trabajador))
trabajador_bp.route("/api/trabajadores/<int:id>", methods=["GET"])(login_required(mostrar_trabajador))
trabajador_bp.route("/api/trabajadores/<int:id>", methods=["PUT"])(
    login_required(actualizar_trabajador)
)
trabajador_bp.route("/api/trabajadores/<int:id>", methods=["DELETE"])(
    login_required(eliminar_trabajador)
)
trabajador_bp.route("/api/trabajadores/<int:id>/reactivar", methods=["PUT"])(
    login_required(reactivar_trabajador)
)
trabajador_bp.route("/api/search-trabajador/<int:nro_documento>", methods=["GET"])(
    login_required(search_trabajador)
)
