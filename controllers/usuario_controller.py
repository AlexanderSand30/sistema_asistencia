from datetime import datetime

from flask import session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from config.constants import ROLES, PASSWORD_MIN_LENGTH
from models.usuario import db, Usuario
from services.trabajador_service import TrabajadorService


class UsuarioController:

    trabajador_service = TrabajadorService()

    # ---------- HELPERS INTERNOS ----------
    @staticmethod
    def _puede_gestionar(usuario_objetivo):
        return (
            usuario_objetivo.rol != "superadmin" or session.get("rol") == "superadmin"
        )

    @staticmethod
    def _rol_valido(rol):
        return rol in ROLES

    @staticmethod
    def _puede_asignar_rol(rol):
        # Solo un superadmin puede crear/ascender a otro superadmin.
        if rol == "superadmin" and session.get("rol") != "superadmin":
            return False
        return True

    @staticmethod
    def _usuario_existe(nombre_usuario, excluir_id=None):
        # Comparación case-insensitive: evita que "Juan" y "juan"
        # convivan como cuentas "distintas" pero confusamente iguales.
        query = Usuario.query.filter(
            func.lower(Usuario.usuario) == nombre_usuario.lower()
        )
        if excluir_id is not None:
            query = query.filter(Usuario.id != excluir_id)
        return query.first() is not None

    @staticmethod
    def _documento_existe(nro_documento, excluir_id=None):
        if not nro_documento:
            return False
        query = Usuario.query.filter(Usuario.nro_documento == nro_documento)
        if excluir_id is not None:
            query = query.filter(Usuario.id != excluir_id)
        return query.first() is not None

    @staticmethod
    def _trabajador_valido(nro_documento):
        if not nro_documento:
            return False, "Debes asignar el número de documento del trabajador."
        trabajador = UsuarioController.trabajador_service.buscar_por_dni(nro_documento)
        if not trabajador:
            return False, "El número de documento no corresponde a un trabajador activo."
        return True, None

    @staticmethod
    def _escapar_like(texto):
        # Escapa los comodines propios de LIKE/ILIKE para que una
        # búsqueda con "%" o "_" no se interprete como comodín.
        return texto.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")

    @staticmethod
    def _aplicar_estado(usuario, nuevo_estado):
        usuario.estado = nuevo_estado
        usuario.updated_by = session.get("usuario_id")
        if nuevo_estado:
            usuario.deleted_by = None
            usuario.deleted_at = None
        else:
            usuario.deleted_by = session.get("usuario_id")
            usuario.deleted_at = datetime.utcnow()

    # ---------- LISTAR ----------
    @staticmethod
    def listar(busqueda="", estado="activos", pagina=1, por_pagina=10):
        query = Usuario.query
        if session.get("rol") != "superadmin":
            query = query.filter(Usuario.rol != "superadmin")

        if busqueda:
            patron = f"%{UsuarioController._escapar_like(busqueda)}%"
            query = query.filter(
                (Usuario.usuario.ilike(patron, escape="\\"))
                | (Usuario.nombre.ilike(patron, escape="\\"))
                | (Usuario.nro_documento.ilike(patron, escape="\\"))
                | (Usuario.rol.ilike(patron, escape="\\"))
            )

        if estado == "activos":
            query = query.filter(Usuario.estado.is_(True))
        elif estado == "inactivos":
            query = query.filter(Usuario.estado.is_(False))

        return query.order_by(Usuario.id.desc()).paginate(
            page=pagina, per_page=por_pagina
        )

    # ---------- OBTENER ----------
    @staticmethod
    def obtener_por_id(id):
        return Usuario.query.get_or_404(id)

    # ---------- CREAR ----------
    @staticmethod
    def crear(nro_documento, nombre, usuario, password, rol, estado=True):
        if not UsuarioController._rol_valido(rol):
            return None, "Rol no válido."
        if not UsuarioController._puede_asignar_rol(rol):
            return None, "Solo un superadministrador puede crear superadministradores."
        if len(password) < PASSWORD_MIN_LENGTH:
            return (
                None,
                f"La contraseña debe tener al menos {PASSWORD_MIN_LENGTH} caracteres.",
            )

        nombre_usuario = usuario.strip()
        nro_documento = nro_documento.strip()
        valido, error = UsuarioController._trabajador_valido(nro_documento)
        if not valido:
            return None, error
        if len(nro_documento) != 8 or not nro_documento.isdigit():
            return None, "El número de documento debe tener exactamente 8 dígitos."
        if UsuarioController._usuario_existe(nombre_usuario):
            return None, "Ese nombre de usuario ya está en uso."
        if UsuarioController._documento_existe(nro_documento):
            return None, "Ese número de documento ya está en uso."

        nuevo = Usuario(
            nro_documento=nro_documento,
            nombre=nombre.strip(),
            usuario=nombre_usuario,
            rol=rol,
            estado=estado,
            created_by=session.get("usuario_id"),
        )
        nuevo.set_password(password)

        db.session.add(nuevo)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None, "Ese nombre de usuario ya está en uso."

        return nuevo, None

    # ---------- EDITAR ----------
    @staticmethod
    def editar(id, nro_documento, nombre, nombre_usuario, password, rol, estado):
        usuario = Usuario.query.get_or_404(id)

        if not UsuarioController._puede_gestionar(usuario):
            return None, "No tienes permisos para modificar este usuario."
        if not UsuarioController._rol_valido(rol):
            return None, "Rol no válido."
        if not UsuarioController._puede_asignar_rol(rol):
            return None, "Solo un superadministrador puede asignar ese rol."
        if password and len(password) < PASSWORD_MIN_LENGTH:
            return (
                None,
                f"La contraseña debe tener al menos {PASSWORD_MIN_LENGTH} caracteres.",
            )

        nombre_usuario = nombre_usuario.strip()
        nro_documento = nro_documento.strip()
        valido, error = UsuarioController._trabajador_valido(nro_documento)
        if not valido:
            return None, error
        if len(nro_documento) != 8 or not nro_documento.isdigit():
            return None, "El número de documento debe tener exactamente 8 dígitos."
        if UsuarioController._usuario_existe(nombre_usuario, excluir_id=id):
            return None, "Ese nombre de usuario ya está en uso."
        if UsuarioController._documento_existe(nro_documento, excluir_id=id):
            return None, "Ese número de documento ya está en uso."

        usuario.nro_documento = nro_documento
        usuario.nombre = nombre.strip()
        usuario.usuario = nombre_usuario
        usuario.rol = rol
        usuario.updated_by = session.get("usuario_id")

        # Reutiliza la misma lógica de auditoría que usa el toggle,
        # para no duplicar el manejo de deleted_by/deleted_at.
        UsuarioController._aplicar_estado(usuario, estado)

        if password:
            usuario.set_password(password)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None, "Ese nombre de usuario ya está en uso."
        return usuario, None

    # ---------- ELIMINAR (desactivar) ----------
    @staticmethod
    def eliminar(id):
        if id == session.get("usuario_id"):
            return False, "No puedes eliminar tu propio usuario."

        usuario = Usuario.query.get_or_404(id)
        if not UsuarioController._puede_gestionar(usuario):
            return False, "No tienes permisos para desactivar este usuario."
        if not usuario.estado:
            return False, "El usuario ya está inactivo."

        UsuarioController._aplicar_estado(usuario, False)
        db.session.commit()

        return True, None

    # ---------- TOGGLE ESTADO ----------
    @staticmethod
    def toggle_estado(id):
        if id == session.get("usuario_id"):
            return None, "No puedes cambiar el estado de tu propio usuario."

        usuario = Usuario.query.get_or_404(id)
        if not UsuarioController._puede_gestionar(usuario):
            return None, "No tienes permisos para cambiar el estado de este usuario."

        UsuarioController._aplicar_estado(usuario, not usuario.estado)
        db.session.commit()

        return usuario.estado, None
