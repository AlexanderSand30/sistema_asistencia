from datetime import datetime

from user_agents import parse

from config.extensions import db
from flask import request, session, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash

from models.usuario import Usuario
from models.LoginLog import LoginLog


def authenticate():

    usuario_input = request.form.get("usuario", "").strip()
    password = request.form.get("password", "")

    # Validación básica
    if not usuario_input or not password:
        flash("Debe ingresar usuario y contraseña.", "danger")
        return render_template("login.html")

    usuario = Usuario.query.filter_by(usuario=usuario_input).first()

    if not usuario:
        flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("login.html")

    if not usuario.estado:
        flash("El usuario está desactivado.", "danger")
        return render_template("login.html")

    if not check_password_hash(usuario.password, password):
        flash("Usuario o contraseña incorrectos.", "danger")
        return render_template("login.html")

    # Login correcto
    session.clear()

    session["usuario_id"] = usuario.id
    session["nombre"] = usuario.nombre
    session["usuario"] = usuario.usuario
    session["rol"] = usuario.rol

    registrar_login(usuario)

    return redirect(url_for("dashboard"))


def controller_logout():
    session.clear()
    return redirect(url_for("login.login"))


def registrar_login(user):

    ua_string = request.headers.get("User-Agent", "")
    ua = parse(ua_string)

    # Obtener IP
    ip_address = request.headers.get("X-Forwarded-For", request.remote_addr)

    # Si X-Forwarded-For contiene varias IPs,
    # normalmente la primera es la IP original.
    if ip_address and "," in ip_address:
        ip_address = ip_address.split(",")[0].strip()

    log = LoginLog(
        user_id=user.id,
        login_at=datetime.utcnow(),
        username=user.usuario,
        ip_address=ip_address,
        user_agent=ua_string,
        browser=ua.browser.family,
        operating_system=ua.os.family,
        device=ua.device.family,
        success=True,
    )

    db.session.add(log)
    db.session.commit()
