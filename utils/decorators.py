from functools import wraps
from flask import make_response, session, redirect, url_for, flash
from functools import wraps


def no_cache(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):

        response = make_response(view(*args, **kwargs))

        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"

        return response

    return wrapped_view


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "usuario_id" not in session:
            flash("Debes iniciar sesión para acceder.", "warning")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("rol") != "admin":
            flash("No tienes permisos para acceder a esta sección.", "danger")
            return redirect(url_for("login.login"))
        return f(*args, **kwargs)

    return decorated
