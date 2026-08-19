from functools import wraps
from flask import make_response, session, redirect, url_for, flash, render_template


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


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get("rol") not in roles:
                return render_template("403.html"), 403
            return f(*args, **kwargs)

        return decorated

    return decorator


# Nota: como login_required y admin_required se combinan siempre
# apilados (@login_required encima de @admin_required), el orden de
# ejecución es: primero se valida la sesión, luego el rol. Si en algún
# momento se usa admin_required sin login_required, session.get("rol")
# simplemente será None y caerá al 403, así que sigue siendo seguro,
# pero conviene no olvidar login_required por consistencia del mensaje
# de error mostrado al usuario.
admin_required = roles_required("admin", "superadmin")
