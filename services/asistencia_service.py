import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import obtener_conexion
from utils.tiempo import ahora


class AsistenciaService:

    def buscar_trabajador_por_dni(self, dni):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, dni, nombres, apellidos, cargo FROM Trabajador WHERE dni = %s AND estado = 1",
                (dni,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "dni": row[1], "nombres": row[2], "apellidos": row[3], "cargo": row[4]}
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def registrar(self, trabajador_id, obra):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            fecha = ahora().strftime("%Y-%m-%d")
            cursor.execute(
                "INSERT INTO Asistencia (trabajador_id, fecha, estado, obra) VALUES (%s, %s, %s, %s)",
                (trabajador_id, fecha, "Pendiente", obra)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def listar(self, fecha_inicio=None, fecha_fin=None):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            sql = """
                SELECT a.id, a.trabajador_id, t.dni, t.nombres, t.apellidos,
                       a.obra, t.cargo, a.fecha, a.hora_entrada, a.hora_salida, a.estado,
                       a.foto_entrada, a.lat_entrada, a.lng_entrada,
                       a.foto_salida, a.lat_salida, a.lng_salida
                FROM Asistencia a
                INNER JOIN Trabajador t ON a.trabajador_id = t.id
            """
            condiciones = []
            parametros = []

            if fecha_inicio and fecha_fin:
                condiciones.append("a.fecha BETWEEN %s AND %s")
                parametros.extend([fecha_inicio, fecha_fin])

            if condiciones:
                sql += " WHERE " + " AND ".join(condiciones)

            sql += " ORDER BY a.fecha DESC, a.id DESC"

            cursor.execute(sql, parametros)
            return cursor.fetchall()
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def marcar_entrada(self, id, hora_entrada, foto=None, lat=None, lng=None):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute("SELECT hora_entrada FROM Asistencia WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row and row[0] is not None:
                raise Exception("Ya se marcó la entrada anteriormente")

            cursor.execute(
                "UPDATE Asistencia SET hora_entrada=%s, estado=%s, "
                "foto_entrada=%s, lat_entrada=%s, lng_entrada=%s WHERE id=%s",
                (hora_entrada, "Presente", foto, lat, lng, id)
            )
            conn.commit()
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def marcar_salida(self, id, hora_salida, foto=None, lat=None, lng=None):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()

            cursor.execute("SELECT hora_salida FROM Asistencia WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row and row[0] is not None:
                raise Exception("Ya se marcó la salida anteriormente")

            cursor.execute("SELECT hora_entrada FROM Asistencia WHERE id = %s", (id,))
            row = cursor.fetchone()
            if row and row[0] is None:
                raise Exception("Primero debe marcar la entrada")

            cursor.execute(
                "UPDATE Asistencia SET hora_salida=%s, foto_salida=%s, lat_salida=%s, lng_salida=%s WHERE id=%s",
                (hora_salida, foto, lat, lng, id)
            )
            conn.commit()
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()