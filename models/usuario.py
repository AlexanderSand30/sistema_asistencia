from config.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):

    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(
        db.Enum("admin", "supervisor"), nullable=False, default="supervisor"
    )
    estado = db.Column(db.Boolean, nullable=False, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "nombre_completo": self.nombre_completo,
            "email": self.email,
            "rol": self.rol,
            "activo": self.activo,
            "fecha_creacion": (
                self.fecha_creacion.strftime("%Y-%m-%d %H:%M")
                if self.fecha_creacion
                else None
            ),
        }

    def __repr__(self):
        return f"<Usuario {self.usuario}>"
