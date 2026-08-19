from flask import Flask, redirect, url_for, session

from config.database import Config
from config.extensions import db

from routes.usuario_routes import usuario_bp
from routes.trabajador_routes import trabajador_bp
from routes.asistencia_routes import asistencia_bp
from routes.reporte_routes import reporte_bp
from routes.produccion_routes import produccion_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


app.register_blueprint(usuario_bp)
app.register_blueprint(trabajador_bp)
app.register_blueprint(asistencia_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(produccion_bp)


@app.route("/")
def index():

    if not session.get("usuario_id"):
        return redirect(url_for("usuario.login"))

    if session.get("rol") == "admin":
        return redirect(url_for("trabajador.vista_trabajadores"))

    return redirect(url_for("asistencia.vista_asistencia"))


if __name__ == "__main__":
    app.run(debug=True)
