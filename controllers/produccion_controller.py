import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify, session, render_template, make_response
from utils.tiempo import ahora
from services.produccion_service import ProduccionService
from services.pdf_service import html_a_pdf
from services.excel_service import generar_excel

service = ProduccionService()


def obtener_resumen_produccion():
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        fecha_inicio = request.args.get("inicio")
        fecha_fin = request.args.get("fin")
        dni = request.args.get("dni") or None

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Ingrese fecha inicio y fecha fin"}), 400

        datos = service.obtener_resumen(fecha_inicio, fecha_fin, dni)
        return jsonify(datos), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def exportar_pdf_produccion():
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        fecha_inicio = request.args.get("inicio")
        fecha_fin = request.args.get("fin")
        dni = request.args.get("dni") or None

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Ingrese fecha inicio y fecha fin"}), 400

        datos = service.obtener_resumen(fecha_inicio, fecha_fin, dni)

        html_renderizado = render_template(
            "produccion/produccion_pdf.html",
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
        response.headers["Content-Disposition"] = "inline; filename=produccion.pdf"
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def exportar_excel_produccion():
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        fecha_inicio = request.args.get("inicio")
        fecha_fin = request.args.get("fin")
        dni = request.args.get("dni") or None

        if not fecha_inicio or not fecha_fin:
            return jsonify({"error": "Ingrese fecha inicio y fecha fin"}), 400

        datos = service.obtener_resumen(fecha_inicio, fecha_fin, dni)

        encabezados = ["DNI", "Nombres", "Apellidos", "Cargo", "Horas Trabajadas", "Horas Extra", "Faltas"]
        filas = [[d["dni"], d["nombres"], d["apellidos"], d["cargo"],
                  d["horas_trabajadas"], d["horas_extra"], d["faltas"]] for d in datos]

        excel_bytes = generar_excel(
            titulo=f"Producción {fecha_inicio} al {fecha_fin}",
            encabezados=encabezados,
            filas=filas,
            nombre_hoja="Produccion"
        )

        response = make_response(excel_bytes)
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response.headers["Content-Disposition"] = "attachment; filename=produccion.xlsx"
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500