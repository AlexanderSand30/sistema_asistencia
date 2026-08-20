from config.extensions import db

from sqlalchemy import Boolean, Column, Integer, String


class Trabajador(db.Model):

    __tablename__ = "trabajador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(8), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=True)
    estado = Column(Boolean, nullable=False, default=True)

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __repr__(self):
        return f"<Trabajador {self.dni} - {self.nombre_completo()}>"

