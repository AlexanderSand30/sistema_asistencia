import sys, os, base64
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify, session
from services.asistencia_service import AsistenciaService
from utils.tiempo import ahora

service = AsistenciaService()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_DIR_RELATIVO = os.path.join("uploads", "asistencia")


def _guardar_foto(foto_base64, id, tipo):
    if not foto_base64:
        return None
    carpeta_absoluta = os.path.join(BASE_DIR, "static", UPLOAD_DIR_RELATIVO)
    os.makedirs(carpeta_absoluta, exist_ok=True)

    _, datos = foto_base64.split(",", 1)
    imagen_bytes = base64.b64decode(datos)

    nombre_archivo = f"{id}_{tipo}_{ahora().strftime('%Y%m%d%H%M%S')}.jpg"
    ruta_relativa = os.path.join(UPLOAD_DIR_RELATIVO, nombre_archivo).replace("\\", "/")

    ruta_absoluta = os.path.join(BASE_DIR, "static", ruta_relativa)
    with open(ruta_absoluta, "wb") as f:
        f.write(imagen_bytes)

    return ruta_relativa


def buscar_por_dni(dni):
    if session.get('rol') not in ['admin', 'supervisor']:
        return jsonify({"error": "No autorizado"}), 403
    try:
        trabajador = service.buscar_trabajador_por_dni(dni)
        if trabajador:
            return jsonify(trabajador), 200
        return jsonify({"error": "Trabajador no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def registrar_asistencia():
    if session.get('rol') not in ['admin', 'supervisor']:
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json()
        id_creado = service.registrar(data["trabajador_id"], data["obra"])
        return jsonify({"mensaje": "Asistencia registrada", "id": id_creado}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def listar_asistencias():
    if session.get('rol') not in ['admin', 'supervisor']:
        return jsonify({"error": "No autorizado"}), 403
    try:
        fecha_inicio = request.args.get("fecha_inicio")
        fecha_fin = request.args.get("fecha_fin")

        rows = service.listar(fecha_inicio, fecha_fin)
        data = [{
            "id": r[0], "trabajador_id": r[1], "dni": r[2], "nombres": r[3], "apellidos": r[4],
            "obra": r[5], "cargo": r[6], "fecha": str(r[7]),
            "hora_entrada": str(r[8]) if r[8] else "", "hora_salida": str(r[9]) if r[9] else "",
            "estado": r[10],
            "foto_entrada": r[11], "lat_entrada": float(r[12]) if r[12] is not None else None,
            "lng_entrada": float(r[13]) if r[13] is not None else None,
            "foto_salida": r[14], "lat_salida": float(r[15]) if r[15] is not None else None,
            "lng_salida": float(r[16]) if r[16] is not None else None,
        } for r in rows]
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def marcar_entrada(id):
    if session.get('rol') not in ['admin', 'supervisor']:
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json() or {}
        ruta_foto = _guardar_foto(data.get("foto"), id, "entrada")
        hora_entrada = ahora().strftime("%H:%M:%S")
        service.marcar_entrada(id, hora_entrada, ruta_foto, data.get("lat"), data.get("lng"))
        return jsonify({"mensaje": "Entrada marcada", "hora_entrada": hora_entrada}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def marcar_salida(id):
    if session.get('rol') not in ['admin', 'supervisor']:
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json() or {}
        ruta_foto = _guardar_foto(data.get("foto"), id, "salida")
        hora_salida = ahora().strftime("%H:%M:%S")
        service.marcar_salida(id, hora_salida, ruta_foto, data.get("lat"), data.get("lng"))
        return jsonify({"mensaje": "Salida marcada", "hora_salida": hora_salida}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    