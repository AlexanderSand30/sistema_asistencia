from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    jsonify,
)
from utils.decorators import no_cache, login_required
from controllers.login_controller import authenticate, controller_logout
from controllers.usuario_controller import UsuarioController

usuario_bp = Blueprint("usuario", __name__, url_prefix="/")


@usuario_bp.route("/login", methods=["GET", "POST"])
@no_cache
def login():
    if request.method == "POST":
        return authenticate()

    if session.get("usuario_id"):
        return redirect(url_for("trabajador.vista_trabajadores"))
    return render_template("login.html")


@usuario_bp.route("/logout")
@login_required
def logout():
    return controller_logout()


@usuario_bp.route("usuarios/")
@login_required
# @admin_required
def listar():
    pagina = request.args.get("page", 1, type=int)
    busqueda = request.args.get("q", "")

    usuarios = UsuarioController.listar(busqueda=busqueda, pagina=pagina)
    return render_template("usuarios/index.html", usuarios=usuarios, busqueda=busqueda)


@usuario_bp.route("/crear", methods=["GET", "POST"])
@login_required
# @admin_required
def crear():
    # form = UsuarioForm()

    # if form.validate_on_submit():
    #     nuevo = Usuario(
    #         usuario=form.usuario.data,
    #         nombre_completo=form.nombre_completo.data,
    #         email=form.email.data,
    #         rol=form.rol.data,
    #         activo=form.activo.data,
    #     )
    #     nuevo.set_password(form.password.data)

    #     db.session.add(nuevo)
    #     db.session.commit()

    #     flash("Usuario creado correctamente.", "success")
    return redirect(url_for("usuario.listar"))


# return render_template("usuarios/crear.html", form=form)


@usuario_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
# @admin_required
def editar(id):
    usuario = UsuarioController.obtener_por_id(id)
    # form = UsuarioEditForm(obj=usuario)

    # if form.validate_on_submit():
    #     actualizado, _ = UsuarioController.editar(id, form)
    #     if actualizado:
    #         return redirect(url_for("usuario.listar"))

    # return render_template("usuarios/editar.html", form=form, usuario=usuario)


# ---------- ELIMINAR ----------
@usuario_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
# @admin_required
def eliminar(id):
    UsuarioController.eliminar(id)
    return redirect(url_for("usuario.listar"))


# ---------- TOGGLE ESTADO (AJAX) ----------
@usuario_bp.route("/toggle-estado/<int:id>", methods=["POST"])
@login_required
# @admin_required
def toggle_estado(id):
    resultado, status = UsuarioController.toggle_estado(id)
    return jsonify(resultado), status
