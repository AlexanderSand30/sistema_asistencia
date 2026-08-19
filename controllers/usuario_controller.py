from datetime import datetime
from flask import flash, redirect, url_for, request, jsonify
from models.usuario import db, Usuario


class UsuarioController:
    @staticmethod
    def listar(busqueda="", pagina=1, por_pagina=10):
        query = Usuario.query

        if busqueda:
            query = query.filter(
                (Usuario.usuario.ilike(f"%{busqueda}%"))
                | (Usuario.nombre.ilike(f"%{busqueda}%"))
                | (Usuario.email.ilike(f"%{busqueda}%"))
            )

        return query.order_by(Usuario.id.desc()).paginate(
            page=pagina, per_page=por_pagina
        )

    # ---------- OBTENER ----------
    @staticmethod
    def obtener_por_id(id):
        return Usuario.query.get_or_404(id)

    # ---------- CREAR ----------
    @staticmethod
    def crear(form):
        nuevo = Usuario(
            usuario=form.usuario.data,
            nombre_completo=form.nombre_completo.data,
            email=form.email.data,
            rol=form.rol.data,
            activo=form.activo.data,
        )
        nuevo.set_password(form.password.data)

        db.session.add(nuevo)
        db.session.commit()

        flash("Usuario creado correctamente.", "success")
        return nuevo

    # ---------- EDITAR ----------
    @staticmethod
    def editar(id, form):
        usuario = Usuario.query.get_or_404(id)

        existente_usuario = Usuario.query.filter(
            Usuario.usuario == form.usuario.data, Usuario.id != id
        ).first()
        existente_email = Usuario.query.filter(
            Usuario.email == form.email.data, Usuario.id != id
        ).first()

        if existente_usuario:
            flash("Ese nombre de usuario ya está en uso.", "danger")
            return None, usuario

        if existente_email:
            flash("Ese email ya está en uso.", "danger")
            return None, usuario

        usuario.usuario = form.usuario.data
        usuario.nombre_completo = form.nombre_completo.data
        usuario.email = form.email.data
        usuario.rol = form.rol.data
        usuario.activo = form.activo.data

        if form.password.data:
            usuario.set_password(form.password.data)

        db.session.commit()
        flash("Usuario actualizado correctamente.", "success")
        return usuario, usuario

    # ---------- ELIMINAR ----------
    @staticmethod
    def eliminar(id):
        if id == current_user.id:
            flash("No puedes eliminar tu propio usuario.", "danger")
            return False

        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()

        flash("Usuario eliminado correctamente.", "success")
        return True

    # ---------- TOGGLE ESTADO ----------
    @staticmethod
    def toggle_estado(id):
        if id == current_user.id:
            return {"ok": False, "mensaje": "No puedes desactivarte a ti mismo."}, 400

        usuario = Usuario.query.get_or_404(id)
        usuario.activo = not usuario.activo
        db.session.commit()

        return {"ok": True, "activo": usuario.activo}, 200
