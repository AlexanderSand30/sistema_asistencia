from flask import Blueprint, render_template, session, redirect, url_for
from controllers.produccion_controller import (
    obtener_resumen_produccion, exportar_pdf_produccion, exportar_excel_produccion
)

produccion_bp = Blueprint("produccion", __name__)


@produccion_bp.route("/produccion", methods=["GET"])
def vista_produccion():
    if not session.get("usuario_id"):
        return redirect(url_for("usuario.login"))
    if session.get("rol") != "admin":
        return "No autorizado", 403
    return render_template("produccion/index.html")


produccion_bp.route("/api/produccion", methods=["GET"])(obtener_resumen_produccion)
produccion_bp.route("/produccion/pdf", methods=["GET"])(exportar_pdf_produccion)
produccion_bp.route("/produccion/excel", methods=["GET"])(exportar_excel_produccion)