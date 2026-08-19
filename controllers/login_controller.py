from flask import request, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash
from models.usuario import Usuario


def authenticate():

    usuario = request.form.get("usuario", "").strip()
    password = request.form.get("password", "")

    # Validación básica
    if not usuario or not password:
        flash("Debe ingresar usuario y contraseña.", "danger")
        return render_template("login.html")

    usuario = Usuario.query.filter_by(usuario=usuario).first()

    if not usuario:
        flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("login.html")

    if not usuario.estado:
        flash("El usuario está desactivado.", "danger")
        return render_template("login.html")

    if not check_password_hash(usuario.password, password):
        flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("login.html")

    session.clear()

    session["usuario_id"] = usuario.id
    session["nombre"] = usuario.nombre
    session["usuario"] = usuario.usuario
    session["rol"] = usuario.rol

    return redirect(url_for("dashboard"))


def controller_logout():
    session.clear()
    return redirect(url_for("login.login"))
