from flask import Blueprint, render_template
from controllers.usuario_controller import login, logout

usuario_bp = Blueprint("usuario", __name__)

usuario_bp.route("/login", methods=["GET"])(lambda: render_template("login.html"))
usuario_bp.route("/login", methods=["POST"])(login)
usuario_bp.route("/logout", methods=["GET"])(logout)