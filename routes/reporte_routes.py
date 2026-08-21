from flask import Blueprint, render_template
from controllers.reporte_controller import obtener_datos_reporte, exportar_pdf
from utils.decorators import login_required

reporte_bp = Blueprint("reporte", __name__)


@reporte_bp.route("/reportes", methods=["GET"])
@login_required
def vista_reportes():
    return render_template("reportes/index.html")


reporte_bp.route("/api/reportes", methods=["GET"])(obtener_datos_reporte)
reporte_bp.route("/reportes/pdf", methods=["GET"])(exportar_pdf)
