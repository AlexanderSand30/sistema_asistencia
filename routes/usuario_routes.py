from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
)

from config.constants import ROLES, PASSWORD_MIN_LENGTH
from utils.decorators import login_required, admin_required
from controllers.usuario_controller import UsuarioController

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")


@usuario_bp.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    usuario = UsuarioController.obtener_perfil()
    es_privilegiado = session.get("rol") in ("admin", "superadmin")

    if request.method == "POST":
        accion = request.form.get("accion")
        if accion == "password":
            password_nueva = request.form.get("password_nueva", "")
            password_confirmacion = request.form.get("password_confirmacion", "")
            if password_nueva != password_confirmacion:
                flash("Las nuevas contraseñas no coinciden.", "danger")
                return redirect(url_for("usuario.perfil"))

            error = UsuarioController.cambiar_password(
                usuario,
                request.form.get("password_actual", ""),
                password_nueva,
            )
            if error:
                flash(error, "danger")
            else:
                flash("Contraseña actualizada correctamente.", "success")
        elif accion == "datos" and es_privilegiado:
            error = UsuarioController.actualizar_perfil(
                usuario,
                request.form.get("nro_documento", ""),
                request.form.get("nombre", ""),
                request.form.get("usuario", ""),
            )
            if error:
                flash(error, "danger")
            else:
                flash("Perfil actualizado correctamente.", "success")
        else:
            flash("No tienes permisos para realizar esa acción.", "danger")
        return redirect(url_for("usuario.perfil"))

    return render_template(
        "usuarios/perfil.html", usuario=usuario, es_privilegiado=es_privilegiado
    )


@usuario_bp.route("/")
@login_required
@admin_required
def listar():
    pagina = request.args.get("page", 1, type=int)
    busqueda = request.args.get("q", "")
    estado = request.args.get("estado", "activos")
    if estado not in ("activos", "inactivos", "todos"):
        estado = "activos"

    usuarios = UsuarioController.listar(busqueda=busqueda, estado=estado, pagina=pagina)
    return render_template(
        "usuarios/index.html", usuarios=usuarios, busqueda=busqueda, estado=estado,
    )


@usuario_bp.route("/crear", methods=["GET", "POST"])
@login_required
@admin_required
def crear():
    if request.method == "GET":
        return redirect(url_for("usuario.listar"))

    nro_documento = request.form.get("nro_documento", "").strip()
    nombre = request.form.get("nombre", "").strip()
    usuario = request.form.get("usuario", "").strip()
    password = request.form.get("password", "")
    rol = request.form.get("rol", "supervisor")

    if (
        not nombre
        or not usuario
        or len(password) < PASSWORD_MIN_LENGTH
        or rol not in ROLES
    ):
        flash("Completa todos los campos obligatorios.", "danger")
        return redirect(url_for("usuario.listar"))

    _, error = UsuarioController.crear(
        nro_documento, nombre, usuario, password, rol
    )
    (
        flash(error, "danger")
        if error
        else flash("Usuario creado correctamente.", "success")
    )
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar(id):
    if request.method == "GET":
        return redirect(url_for("usuario.listar"))

    nombre = request.form.get("nombre", "").strip()
    nro_documento = request.form.get("nro_documento", "").strip()
    nombre_usuario = request.form.get("usuario", "").strip()
    password = request.form.get("password", "")
    rol = request.form.get("rol", "supervisor")
    estado = request.form.get("estado") == "1"

    if not nombre or not nombre_usuario or rol not in ROLES:
        flash("Completa todos los campos obligatorios.", "danger")
        return redirect(url_for("usuario.listar"))

    _, error = UsuarioController.editar(
        id, nro_documento, nombre, nombre_usuario, password, rol, estado
    )
    (
        flash(error, "danger")
        if error
        else flash("Usuario actualizado correctamente.", "success")
    )
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/eliminar/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar(id):
    eliminado, error = UsuarioController.eliminar(id)
    if error:
        flash(error, "danger")
    elif eliminado:
        flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("usuario.listar"))


@usuario_bp.route("/toggle-estado/<int:id>", methods=["POST"])
@login_required
@admin_required
def toggle_estado(id):
    estado, error = UsuarioController.toggle_estado(id)
    if error:
        flash(error, "danger")
    elif estado:
        flash("Usuario activado correctamente.", "success")
    else:
        flash("Usuario desactivado correctamente.", "success")
    return redirect(url_for("usuario.listar"))
