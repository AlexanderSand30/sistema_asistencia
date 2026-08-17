import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.conexion import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioService:

    def autenticar(self, usuario, password_ingresado):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, nombre, usuario, password, rol FROM Usuario WHERE usuario = %s AND estado = 1",
                (usuario,)
            )
            row = cursor.fetchone()

            if not row:
                return None

            id, nombre, usuario_bd, password_hash, rol = row

            if check_password_hash(password_hash, password_ingresado):
                return {"id": id, "nombre": nombre, "usuario": usuario_bd, "rol": rol}

            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()

    def crear_usuario(self, nombre, usuario, password_plano, rol="supervisor"):
        conn, cursor = None, None
        try:
            conn = obtener_conexion()
            cursor = conn.cursor()
            password_hash = generate_password_hash(password_plano)
            cursor.execute(
                "INSERT INTO Usuario (nombre, usuario, password, rol) VALUES (%s, %s, %s, %s)",
                (nombre, usuario, password_hash, rol)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception:
            if conn: conn.rollback()
            raise
        finally:
            if cursor: cursor.close()
            if conn: conn.close()