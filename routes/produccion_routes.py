from flask import Blueprint, render_template
from controllers.produccion_controller import (
    obtener_resumen_produccion, exportar_pdf_produccion, exportar_excel_produccion
)
from utils.decorators import login_required, admin_required

produccion_bp = Blueprint("produccion", __name__)


@produccion_bp.route("/produccion", methods=["GET"])
@login_required
@admin_required
def vista_produccion():
    return render_template("produccion/index.html")


produccion_bp.route("/api/produccion", methods=["GET"])(obtener_resumen_produccion)
produccion_bp.route("/produccion/pdf", methods=["GET"])(exportar_pdf_produccion)
produccion_bp.route("/produccion/excel", methods=["GET"])(exportar_excel_produccion)