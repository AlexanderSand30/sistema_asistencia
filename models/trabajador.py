from config.extensions import db

from sqlalchemy import Boolean, Column, Integer, String, Date


class Trabajador(db.Model):

    __tablename__ = "trabajador"

    id = Column(Integer, primary_key=True, autoincrement=True)
    dni = Column(String(8), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    cargo = Column(String(100), nullable=True)
    fecha_nac = Column(Date, nullable=False)
    fecha_ingreso = Column(Date, nullable=False)
    fecha_cese = Column(Date, nullable=True)
    estado = Column(Boolean, nullable=False, default=True)

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __repr__(self):
        return f"<Trabajador {self.dni} - {self.nombre_completo()}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "dni": self.dni,
            "cargo": self.cargo,
            "fecha_nac": self.fecha_nac.isoformat() if self.fecha_nac else None,
            "fecha_ingreso": (
                self.fecha_ingreso.isoformat() if self.fecha_ingreso else None
            ),
            "fecha_cese": self.fecha_cese.isoformat() if self.fecha_cese else None,
            "estado": self.estado,
        }
