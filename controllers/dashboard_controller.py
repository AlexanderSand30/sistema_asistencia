from flask import session
from sqlalchemy import func

from models.asistencia_model import Asistencia
from models.trabajador import Trabajador
from models.usuario import Usuario


def obtener_datos_dashboard():
    rol = session.get("rol")
    es_administrador = rol in ("admin", "superadmin")

    if es_administrador:
        metricas = {
            "trabajadores_activos": Trabajador.query.filter_by(estado=True).count(),
            "trabajadores_inactivos": Trabajador.query.filter_by(estado=False).count(),
            "usuarios_activos": Usuario.query.filter(
                Usuario.estado.is_(True), Usuario.rol != "superadmin"
            ).count(),
            "asistencias_hoy": Asistencia.query.filter(
                Asistencia.fecha == func.current_date()
            ).count(),
        }
    else:
        usuario = Usuario.query.get(session.get("usuario_id"))
        trabajador = None
        if usuario and usuario.nro_documento:
            trabajador = Trabajador.query.filter_by(
                dni=usuario.nro_documento, estado=True
            ).first()

        usuario_id = session.get("usuario_id")
        metricas = {
            "trabajador": trabajador,
            "mis_asistencias": Asistencia.query.filter_by(
                created_by=usuario_id
            ).count(),
            "mis_asistencias_hoy": Asistencia.query.filter(
                Asistencia.created_by == usuario_id,
                Asistencia.fecha == func.current_date(),
            ).count(),
        }

    return {
        "rol": rol,
        "es_administrador": es_administrador,
        "metricas": metricas,
    }
