import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import obtener_conexion
from models.trabajador_model import Trabajador
from mysql.connector import IntegrityError


class TrabajadorService:

    def listar(self):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, dni, nombres, apellidos, cargo, estado "
                "FROM Trabajador WHERE estado = 1 ORDER BY apellidos"
            )
            return [Trabajador(*row) for row in cursor.fetchall()]
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def listar_inactivos(self):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, dni, nombres, apellidos, cargo, estado "
                "FROM Trabajador WHERE estado = 0 ORDER BY apellidos"
            )
            return [Trabajador(*row) for row in cursor.fetchall()]
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def crear(self, trabajador):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Trabajador (dni, nombres, apellidos, cargo) VALUES (%s, %s, %s, %s)",
                (trabajador.dni, trabajador.nombres, trabajador.apellidos, trabajador.cargo)
            )
            conn.commit()
            return cursor.lastrowid
        except IntegrityError:
            if conn: conn.rollback()
            raise Exception(f"Ya existe un trabajador registrado con el DNI {trabajador.dni}")
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def actualizar(self, trabajador):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE Trabajador SET dni=%s, nombres=%s, apellidos=%s, cargo=%s WHERE id=%s",
                (trabajador.dni, trabajador.nombres, trabajador.apellidos, trabajador.cargo, trabajador.id)
            )
            conn.commit()
        except IntegrityError:
            if conn: conn.rollback()
            raise Exception(f"El DNI {trabajador.dni} ya pertenece a otro trabajador")
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def eliminar(self, id):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("UPDATE Trabajador SET estado = 0 WHERE id = %s", (id,))
            conn.commit()
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def reactivar(self, id):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("UPDATE Trabajador SET estado = 1 WHERE id = %s", (id,))
            conn.commit()
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
            