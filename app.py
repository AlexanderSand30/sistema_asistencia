from flask import Flask, redirect, render_template, url_for, session

from config.database import Config
from config.extensions import db
from controllers.dashboard_controller import obtener_datos_dashboard

from routes.login_routes import login_bp
from routes.usuario_routes import usuario_bp
from routes.trabajador_routes import trabajador_bp
from routes.asistencia_routes import asistencia_bp
from routes.reporte_routes import reporte_bp
from routes.produccion_routes import produccion_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)


app.register_blueprint(login_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(trabajador_bp)
app.register_blueprint(asistencia_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(produccion_bp)


@app.route("/")
def index():

    if not session.get("usuario_id"):
        return redirect(url_for("login.login"))

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if not session.get("usuario_id"):
        return redirect(url_for("login.login"))

    return render_template("dashboard.html", **obtener_datos_dashboard())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
