import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import obtener_conexion


class ReporteService:

    def obtener_reporte(self, fecha_inicio, fecha_fin, dni=None, usuario_id=None):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            sql = """
                SELECT t.dni, t.nombres, t.apellidos, a.obra, t.cargo,
                       a.fecha, a.hora_entrada, a.hora_salida, a.estado
                FROM Asistencia a
                INNER JOIN Trabajador t ON a.trabajador_id = t.id
                WHERE a.fecha BETWEEN %s AND %s
            """
            parametros = [fecha_inicio, fecha_fin]

            if usuario_id is not None:
                sql += " AND a.created_by = %s"
                parametros.append(usuario_id)

            if dni:
                sql += " AND t.dni = %s"
                parametros.append(dni)

            sql += " ORDER BY a.fecha DESC, t.apellidos"

            cursor.execute(sql, parametros)
            rows = cursor.fetchall()

            return [{
                "dni": r[0], "nombres": r[1], "apellidos": r[2], "obra": r[3], "cargo": r[4],
                "fecha": str(r[5]),
                "hora_entrada": str(r[6]) if r[6] else "--:--",
                "hora_salida": str(r[7]) if r[7] else "--:--",
                "estado": r[8]
            } for r in rows]
        finally:
            if cursor: cursor.close()
            if conn: conn.close()