from flask import Blueprint, render_template, session, redirect, url_for
from controllers.reporte_controller import obtener_datos_reporte, exportar_pdf

reporte_bp = Blueprint("reporte", __name__)


@reporte_bp.route("/reportes", methods=["GET"])
def vista_reportes():
    if not session.get("usuario_id"):
        return redirect(url_for("usuario.login"))
    return render_template("reportes/index.html")


reporte_bp.route("/api/reportes", methods=["GET"])(obtener_datos_reporte)
reporte_bp.route("/reportes/pdf", methods=["GET"])(exportar_pdf)