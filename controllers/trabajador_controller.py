import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify, session
from services.trabajador_service import TrabajadorService
from models.trabajador_model import Trabajador

service = TrabajadorService()


def _validar_dni(dni):
    if not dni or not dni.isdigit() or len(dni) != 8:
        return "El DNI debe contener exactamente 8 números"
    return None


def listar_trabajadores():
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        trabajadores = service.listar()
        return jsonify([{
            "id": t.id, "dni": t.dni, "nombres": t.nombres,
            "apellidos": t.apellidos, "cargo": t.cargo, "estado": t.estado
        } for t in trabajadores]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def listar_inactivos():
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        trabajadores = service.listar_inactivos()
        return jsonify([{
            "id": t.id, "dni": t.dni, "nombres": t.nombres,
            "apellidos": t.apellidos, "cargo": t.cargo, "estado": t.estado
        } for t in trabajadores]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def crear_trabajador():
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json()
        error_dni = _validar_dni(data.get("dni", ""))
        if error_dni:
            return jsonify({"error": error_dni}), 400
        t = Trabajador(None, data["dni"], data["nombres"], data["apellidos"], data["cargo"])
        service.crear(t)
        return jsonify({"mensaje": "Trabajador creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def actualizar_trabajador(id):
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json()
        error_dni = _validar_dni(data.get("dni", ""))
        if error_dni:
            return jsonify({"error": error_dni}), 400
        t = Trabajador(id, data["dni"], data["nombres"], data["apellidos"], data["cargo"])
        service.actualizar(t)
        return jsonify({"mensaje": "Trabajador actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def eliminar_trabajador(id):
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        service.eliminar(id)
        return jsonify({"mensaje": "Trabajador eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def reactivar_trabajador(id):
    if session.get('rol') != 'admin':
        return jsonify({"error": "No autorizado"}), 403
    try:
        service.reactivar(id)
        return jsonify({"mensaje": "Trabajador reactivado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500