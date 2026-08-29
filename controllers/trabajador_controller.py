import sys, os
import math
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import request, jsonify, session
from services.trabajador_service import TrabajadorService
from models.trabajador import Trabajador

service = TrabajadorService()


def _validar_dni(dni):
    if not dni or not dni.isdigit() or len(dni) != 8:
        return "El DNI debe contener exactamente 8 números"
    return None


def _obtener_fechas(data):
    try:
        fecha_nac = date.fromisoformat(data.get("fecha_nac", ""))
    except ValueError:
        return None, None, "La fecha de nacimiento es obligatoria y debe ser válida"

    try:
        fecha_ingreso = date.fromisoformat(data.get("fecha_ingreso", ""))
    except ValueError:
        return None, None, "La fecha de ingreso es obligatoria y debe ser válida"

    fecha_cese_texto = data.get("fecha_cese", "") or ""
    try:
        fecha_cese = date.fromisoformat(fecha_cese_texto) if fecha_cese_texto else None
    except ValueError:
        return None, None, "La fecha de cese debe ser válida"

    if fecha_cese and fecha_cese < fecha_ingreso:
        return (
            None,
            None,
            "La fecha de cese no puede ser anterior a la fecha de ingreso",
        )
    return fecha_ingreso, fecha_cese, fecha_nac, None


def _serializar_trabajadores(trabajadores):
    return [
        {
            "id": t.id,
            "dni": t.dni,
            "nombres": t.nombres,
            "apellidos": t.apellidos,
            "cargo": t.cargo,
            "fecha_nac": t.fecha_nac.isoformat() if t.fecha_nac else None,
            "fecha_ingreso": t.fecha_ingreso.isoformat() if t.fecha_ingreso else None,
            "fecha_cese": t.fecha_cese.isoformat() if t.fecha_cese else None,
            "estado": t.estado,
        }
        for t in trabajadores
    ]


def _paginar_datos(items, page, per_page):
    per_page = max(1, int(per_page))
    page = max(1, int(page))
    total = len(items)
    total_pages = max(1, math.ceil(total / per_page)) if total else 1
    if page > total_pages and total:
        page = total_pages
    inicio = (page - 1) * per_page
    fin = inicio + per_page
    return {
        "items": items[inicio:fin],
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
    }


def listar_trabajadores():
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        trabajadores = service.listar()
        payload = _paginar_datos(_serializar_trabajadores(trabajadores), page, per_page)
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def listar_inactivos():
    if session.get("rol") not in ("admin", "superadmin"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 8, type=int)
        trabajadores = service.listar_inactivos()
        payload = _paginar_datos(_serializar_trabajadores(trabajadores), page, per_page)
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def mostrar_trabajador(id):
    try:
        trabajador = Trabajador.query.filter_by(id=id).first()
        return jsonify(trabajador.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def crear_trabajador():
    if session.get("rol") not in ("admin", "superadmin"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json()
        error_dni = _validar_dni(data.get("dni", ""))
        if error_dni:
            return jsonify({"error": error_dni}), 400
        fecha_ingreso, fecha_cese, fecha_nac, error_fechas = _obtener_fechas(data)
        if error_fechas:
            return jsonify({"error": error_fechas}), 400
        t = Trabajador(
            dni=data["dni"],
            nombres=data["nombres"],
            apellidos=data["apellidos"],
            cargo=data["cargo"],
            fecha_nac=fecha_nac,
            fecha_ingreso=fecha_ingreso,
            fecha_cese=fecha_cese,
            created_by=session.get("usuario_id"),
        )
        service.crear(t)
        return jsonify({"mensaje": "Trabajador creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def actualizar_trabajador(id):
    if session.get("rol") not in ("admin", "superadmin"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        data = request.get_json()
        error_dni = _validar_dni(data.get("dni", ""))
        if error_dni:
            return jsonify({"error": error_dni}), 400
        fecha_ingreso, fecha_cese, fecha_nac, error_fechas = _obtener_fechas(data)
        if error_fechas:
            return jsonify({"error": error_fechas}), 400
        t = Trabajador(
            id=id,
            dni=data["dni"],
            nombres=data["nombres"],
            apellidos=data["apellidos"],
            cargo=data["cargo"],
            fecha_nac=fecha_nac,
            fecha_ingreso=fecha_ingreso,
            fecha_cese=fecha_cese,
        )
        service.actualizar(t)
        return jsonify({"mensaje": "Trabajador actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def eliminar_trabajador(id):
    if session.get("rol") not in ("admin", "superadmin"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        service.eliminar(id)
        return jsonify({"mensaje": "Trabajador eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def reactivar_trabajador(id):
    if session.get("rol") not in ("admin", "superadmin"):
        return jsonify({"error": "No autorizado"}), 403
    try:
        service.reactivar(id)
        return jsonify({"mensaje": "Trabajador reactivado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def search_trabajador(nro_documento):
    try:
        trabajador = Trabajador.query.filter_by(dni=nro_documento).first()
        return jsonify(trabajador.to_dict()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
