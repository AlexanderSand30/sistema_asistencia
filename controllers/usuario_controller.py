import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, jsonify, session, redirect, url_for
from services.usuario_service import UsuarioService

service = UsuarioService()


def login():
    try:
        data = request.get_json()
        usuario = data.get("usuario")
        password = data.get("password")

        resultado = service.autenticar(usuario, password)

        if not resultado:
            return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

        session["usuario_id"] = resultado["id"]
        session["nombre"] = resultado["nombre"]
        session["rol"] = resultado["rol"]

        return jsonify({"mensaje": "Login exitoso", "rol": resultado["rol"]}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def logout():
    session.clear()
    return redirect(url_for("usuario.login"))
