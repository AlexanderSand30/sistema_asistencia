import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import obtener_conexion
from datetime import datetime, timedelta

HORAS_SEMANALES_LEGALES = 48


class ProduccionService:

    def obtener_resumen(self, fecha_inicio, fecha_fin, dni=None):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            # 1. Trabajadores activos (filtrados por DNI si se indicó)
            sql_trab = "SELECT id, dni, nombres, apellidos, cargo FROM Trabajador WHERE estado = 1"
            params_trab = []
            if dni:
                sql_trab += " AND dni = %s"
                params_trab.append(dni)
            cursor.execute(sql_trab, params_trab)
            trabajadores = cursor.fetchall()

            if not trabajadores:
                return []

            ids_trabajadores = [t[0] for t in trabajadores]

            # 2. Todas las asistencias de esos trabajadores en el rango
            formato_ids = ",".join(["%s"] * len(ids_trabajadores))
            cursor.execute(f"""
                SELECT trabajador_id, fecha, hora_entrada, hora_salida
                FROM Asistencia
                WHERE trabajador_id IN ({formato_ids})
                  AND fecha BETWEEN %s AND %s
            """, ids_trabajadores + [fecha_inicio, fecha_fin])
            asistencias = cursor.fetchall()

            # Mapa (trabajador_id, fecha) -> lista de marcados ese día
            # (lista, no un solo valor, porque un trabajador puede tener varios registros el mismo día)
            mapa_asistencia = {}
            for trabajador_id, fecha, hora_entrada, hora_salida in asistencias:
                clave = (trabajador_id, fecha)
                mapa_asistencia.setdefault(clave, []).append((hora_entrada, hora_salida))

            # 3. Recorrer día por día el rango (de lunes a sábado, domingo se omite)
            fecha_actual = self._a_date(fecha_inicio)
            fecha_limite = self._a_date(fecha_fin)

            # acumulador: (trabajador_id, (año, n_semana_iso)) -> {"horas": float, "faltas": int}
            acumulado_semanal = {}

            dia = fecha_actual
            while dia <= fecha_limite:
                dia_semana = dia.weekday()  # 0=lunes ... 5=sábado, 6=domingo

                if dia_semana != 6:
                    semana_key = dia.isocalendar()[:2]

                    for trabajador_id in ids_trabajadores:
                        clave = (trabajador_id, semana_key)
                        acumulado_semanal.setdefault(clave, {"horas": 0.0, "faltas": 0})

                        registros_dia = mapa_asistencia.get((trabajador_id, dia))

                        if not registros_dia:
                            acumulado_semanal[clave]["faltas"] += 1
                        else:
                            for hora_entrada, hora_salida in registros_dia:
                                if hora_entrada and hora_salida:
                                    horas = self._calcular_horas_dia(hora_entrada, hora_salida, dia_semana)
                                    acumulado_semanal[clave]["horas"] += horas

                dia += timedelta(days=1)

            # 4. Calcular horas extra POR SEMANA, y consolidar por trabajador
            resumen = {t[0]: {"horas_trabajadas": 0.0, "horas_extra": 0.0, "faltas": 0} for t in trabajadores}

            for (trabajador_id, semana_key), datos in acumulado_semanal.items():
                extra_semana = max(0, datos["horas"] - HORAS_SEMANALES_LEGALES)
                resumen[trabajador_id]["horas_trabajadas"] += datos["horas"]
                resumen[trabajador_id]["horas_extra"] += extra_semana
                resumen[trabajador_id]["faltas"] += datos["faltas"]

            # 5. Armar resultado final con los datos del trabajador
            resultado = []
            for id_, dni_, nombres, apellidos, cargo in trabajadores:
                d = resumen[id_]
                resultado.append({
                    "dni": dni_, "nombres": nombres, "apellidos": apellidos, "cargo": cargo,
                    "horas_trabajadas": round(d["horas_trabajadas"], 2),
                    "horas_extra": round(d["horas_extra"], 2),
                    "faltas": d["faltas"]
                })
            return resultado
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def _calcular_horas_dia(self, hora_entrada, hora_salida, dia_semana):
        """Horas trabajadas en un día. Resta 1h de almuerzo de lunes a viernes (no el sábado)."""
        segundos = hora_salida.total_seconds() - hora_entrada.total_seconds()
        horas = segundos / 3600
        if horas <= 0:
            return 0
        if dia_semana <= 4:  # lunes(0) a viernes(4)
            horas = max(0, horas - 1)
        return horas

    def _a_date(self, valor):
        if isinstance(valor, str):
            return datetime.strptime(valor, "%Y-%m-%d").date()
        return valor