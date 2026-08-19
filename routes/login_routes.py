from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
)
from utils.decorators import no_cache, login_required
from controllers.login_controller import authenticate, controller_logout

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
@no_cache
def login():
    if request.method == "POST":
        return authenticate()

    if session.get("usuario_id"):
        return redirect(url_for("trabajador.vista_trabajadores"))
    return render_template("login.html")


@login_bp.route("/logout")
@login_required
def logout():
    return controller_logout()
