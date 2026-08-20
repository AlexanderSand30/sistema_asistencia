from datetime import datetime

from config.extensions import db
from config.constants import ROLES
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Boolean,
    DateTime,
    ForeignKey,
    text,
)
from sqlalchemy.orm import relationship


class Usuario(db.Model):

    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nro_documento = Column(String(15), nullable=True, unique=True)
    nombre = Column(String(100), nullable=False)
    usuario = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    rol = Column(
        Enum(*ROLES),
        nullable=False,
        default="operador",
    )
    estado = Column(Boolean, nullable=False, default=True)
    created_by = Column(Integer, ForeignKey("usuario.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("usuario.id"), nullable=True)
    deleted_by = Column(Integer, ForeignKey("usuario.id"), nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    # OJO: "server_onupdate" solo es metadata para SQLAlchemy, no genera
    # ningún "ON UPDATE" en la base de datos. Para que updated_at se
    # refresque de verdad en cada UPDATE, el refresco tiene que hacerlo
    # el propio ORM con `onupdate=`.
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
    )

    deleted_at = Column(DateTime, nullable=True)

    # Relaciones de auditoría
    creador = relationship(
        "Usuario",
        foreign_keys=[created_by],
        remote_side=[id],
    )

    modificador = relationship(
        "Usuario",
        foreign_keys=[updated_by],
        remote_side=[id],
    )

    eliminador = relationship(
        "Usuario",
        foreign_keys=[deleted_by],
        remote_side=[id],
    )

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "nro_documento": self.nro_documento,
            "usuario": self.usuario,
            "nombre": self.nombre,
            "rol": self.rol,
            "estado": self.estado,
        }

    def __repr__(self):
        return f"<Usuario {self.usuario}>"
