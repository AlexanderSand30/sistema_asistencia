from datetime import datetime, time, timedelta

from models.asistencia_model import Asistencia
from models.trabajador import Trabajador

HORAS_SEMANALES_LEGALES = 48


class ProduccionService:

    def obtener_resumen(self, fecha_inicio, fecha_fin, dni=None):
        fecha_inicio = self._a_date(fecha_inicio)
        fecha_fin = self._a_date(fecha_fin)

        query = Trabajador.query.filter_by(estado=True)
        if dni:
            query = query.filter(Trabajador.dni == dni)
        trabajadores = query.order_by(Trabajador.apellidos).all()
        if not trabajadores:
            return []

        ids_trabajadores = [trabajador.id for trabajador in trabajadores]
        asistencias = Asistencia.query.filter(
            Asistencia.trabajador_id.in_(ids_trabajadores),
            Asistencia.fecha.between(fecha_inicio, fecha_fin),
        ).all()

        mapa_asistencia = {}
        for asistencia in asistencias:
            clave = (asistencia.trabajador_id, asistencia.fecha)
            mapa_asistencia.setdefault(clave, []).append(
                (asistencia.hora_entrada, asistencia.hora_salida)
            )

        acumulado_semanal = {}
        dia = fecha_inicio
        while dia <= fecha_fin:
            dia_semana = dia.weekday()
            if dia_semana != 6:
                semana_key = dia.isocalendar()[:2]
                for trabajador_id in ids_trabajadores:
                    clave = (trabajador_id, semana_key)
                    acumulado_semanal.setdefault(
                        clave, {"horas": 0.0, "faltas": 0}
                    )
                    registros_dia = mapa_asistencia.get((trabajador_id, dia))
                    if not registros_dia:
                        acumulado_semanal[clave]["faltas"] += 1
                    else:
                        for hora_entrada, hora_salida in registros_dia:
                            if hora_entrada and hora_salida:
                                acumulado_semanal[clave]["horas"] += self._calcular_horas_dia(
                                    hora_entrada, hora_salida, dia_semana
                                )
            dia += timedelta(days=1)

        resumen = {
            trabajador.id: {"horas_trabajadas": 0.0, "horas_extra": 0.0, "faltas": 0}
            for trabajador in trabajadores
        }
        for (trabajador_id, _), datos in acumulado_semanal.items():
            resumen[trabajador_id]["horas_trabajadas"] += datos["horas"]
            resumen[trabajador_id]["horas_extra"] += max(
                0, datos["horas"] - HORAS_SEMANALES_LEGALES
            )
            resumen[trabajador_id]["faltas"] += datos["faltas"]

        return [
            {
                "dni": trabajador.dni,
                "nombres": trabajador.nombres,
                "apellidos": trabajador.apellidos,
                "cargo": trabajador.cargo,
                "horas_trabajadas": round(resumen[trabajador.id]["horas_trabajadas"], 2),
                "horas_extra": round(resumen[trabajador.id]["horas_extra"], 2),
                "faltas": resumen[trabajador.id]["faltas"],
            }
            for trabajador in trabajadores
        ]

    def _calcular_horas_dia(self, hora_entrada, hora_salida, dia_semana):
        """Horas trabajadas en un día. Resta 1h de almuerzo de lunes a viernes (no el sábado)."""
        entrada_segundos = self._a_segundos(hora_entrada)
        salida_segundos = self._a_segundos(hora_salida)
        if salida_segundos < entrada_segundos:
            salida_segundos += 24 * 60 * 60

        segundos = salida_segundos - entrada_segundos
        horas = segundos / 3600
        if horas <= 0:
            return 0
        if dia_semana <= 4:  # lunes(0) a viernes(4)
            horas = max(0, horas - 1)
        return horas

    def _a_segundos(self, valor):
        if isinstance(valor, time):
            return (
                valor.hour * 3600
                + valor.minute * 60
                + valor.second
                + valor.microsecond / 1_000_000
            )
        if isinstance(valor, timedelta):
            return valor.total_seconds()
        raise TypeError(f"Tipo de hora no soportado: {type(valor).__name__}")

    def _a_date(self, valor):
        if isinstance(valor, str):
            return datetime.strptime(valor, "%Y-%m-%d").date()
        return valor