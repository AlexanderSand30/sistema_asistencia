from datetime import time

from config.extensions import db
from models.asistencia_model import Asistencia
from models.trabajador_model import Trabajador
from utils.tiempo import ahora


class AsistenciaService:

    @staticmethod
    def _hora(valor):
        return time.fromisoformat(valor) if isinstance(valor, str) else valor

    @staticmethod
    def _trabajador_dict(trabajador):
        if not trabajador:
            return None
        return {
            "id": trabajador.id,
            "dni": trabajador.dni,
            "nombres": trabajador.nombres,
            "apellidos": trabajador.apellidos,
            "cargo": trabajador.cargo,
        }

    def buscar_trabajador_por_id(self, trabajador_id):
        trabajador = Trabajador.query.filter_by(id=trabajador_id, estado=True).first()
        return self._trabajador_dict(trabajador)

    def buscar_trabajador_por_dni(self, dni):
        trabajador = Trabajador.query.filter_by(dni=dni, estado=True).first()
        return self._trabajador_dict(trabajador)

    def registrar(self, trabajador_id, obra, usuario_id):
        asistencia = Asistencia(
            trabajador_id=trabajador_id,
            fecha=ahora().date(),
            estado="Pendiente",
            obra=obra,
            created_by=usuario_id,
        )
        db.session.add(asistencia)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        return asistencia.id

    def listar(self, fecha_inicio=None, fecha_fin=None, usuario_id=None, pagina=1, por_pagina=10):
        query = db.session.query(Asistencia, Trabajador).join(
            Trabajador, Asistencia.trabajador_id == Trabajador.id
        )

        if fecha_inicio and fecha_fin:
            query = query.filter(Asistencia.fecha.between(fecha_inicio, fecha_fin))
        if usuario_id is not None:
            query = query.filter(Asistencia.created_by == usuario_id)

        paginacion = query.order_by(Asistencia.fecha.desc(), Asistencia.id.desc()).paginate(
            page=pagina, per_page=por_pagina, error_out=False
        )
        items = [
            (
                asistencia.id,
                asistencia.trabajador_id,
                trabajador.dni,
                trabajador.nombres,
                trabajador.apellidos,
                asistencia.obra,
                trabajador.cargo,
                asistencia.fecha,
                asistencia.hora_entrada,
                asistencia.hora_salida,
                asistencia.estado,
                asistencia.foto_entrada,
                asistencia.lat_entrada,
                asistencia.lng_entrada,
                asistencia.foto_salida,
                asistencia.lat_salida,
                asistencia.lng_salida,
            )
            for asistencia, trabajador in paginacion.items
        ]
        return {
            "items": items,
            "pagina": paginacion.page,
            "por_pagina": paginacion.per_page,
            "total": paginacion.total,
            "total_paginas": paginacion.pages,
        }

    def marcar_entrada(self, id, hora_entrada, foto=None, lat=None, lng=None, usuario_id=None):
        query = Asistencia.query.filter_by(id=id)
        if usuario_id is not None:
            query = query.filter_by(created_by=usuario_id)
        asistencia = query.first()
        if not asistencia:
            raise Exception("Marcación no encontrada o no autorizada")
        if asistencia.hora_entrada is not None:
            raise Exception("Ya se marcó la entrada anteriormente")

        asistencia.hora_entrada = self._hora(hora_entrada)
        asistencia.estado = "Presente"
        asistencia.foto_entrada = foto
        asistencia.lat_entrada = lat
        asistencia.lng_entrada = lng
        db.session.commit()

    def marcar_salida(self, id, hora_salida, foto=None, lat=None, lng=None, usuario_id=None):
        query = Asistencia.query.filter_by(id=id)
        if usuario_id is not None:
            query = query.filter_by(created_by=usuario_id)
        asistencia = query.first()
        if not asistencia:
            raise Exception("Marcación no encontrada o no autorizada")
        if asistencia.hora_salida is not None:
            raise Exception("Ya se marcó la salida anteriormente")
        if asistencia.hora_entrada is None:
            raise Exception("Primero debe marcar la entrada")

        asistencia.hora_salida = self._hora(hora_salida)
        asistencia.foto_salida = foto
        asistencia.lat_salida = lat
        asistencia.lng_salida = lng
        db.session.commit()
