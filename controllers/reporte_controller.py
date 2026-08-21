import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify, render_template, make_response, session
from utils.tiempo import ahora
from services.reporte_service import ReporteService
from services.pdf_service import html_a_pdf

service = ReporteService()


def _es_administrador():
    return session.get("rol") in ("admin", "superadmin")


def _usuario_id_reporte():
    return None if _es_administrador() else session.get("usuario_id")


def obtener_datos_reporte():
    if not session.get("usuario_id"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        fecha_inicio = request.args.get("inicio")
        fecha_fin = request.args.get("fin")
        dni = request.args.get("dni") or None if _es_administrador() else None

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Ingrese fecha inicio y fecha fin"}), 400

        datos = service.obtener_reporte(
            fecha_inicio, fecha_fin, dni, _usuario_id_reporte()
        )
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def exportar_pdf():
    if not session.get("usuario_id"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        fecha_inicio = request.args.get("inicio")
        fecha_fin = request.args.get("fin")
        dni = request.args.get("dni") or None if _es_administrador() else None

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Ingrese fecha inicio y fecha fin"}), 400

        datos = service.obtener_reporte(
            fecha_inicio, fecha_fin, dni, _usuario_id_reporte()
        )

        html_renderizado = render_template(
            "reportes/reporte_pdf.html",
            registros=datos,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            fecha_generacion=ahora().strftime("%d/%m/%Y %H:%M")
        )

        pdf_bytes = html_a_pdf(html_renderizado)
        if pdf_bytes is None:
            return jsonify({"error": "No se pudo generar el PDF"}), 500

        response = make_response(pdf_bytes)
        response.headers["Content-Type"] = "application/pdf"
        response.headers["Content-Disposition"] = "inline; filename=reporte_asistencia.pdf"
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500