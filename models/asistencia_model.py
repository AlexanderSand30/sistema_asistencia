from datetime import datetime

from config.extensions import db

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Time, text
from sqlalchemy.orm import relationship


class Asistencia(db.Model):

    __tablename__ = "asistencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trabajador_id = Column(Integer, ForeignKey("trabajador.id"), nullable=False)
    obra = Column(String(150), nullable=True)
    fecha = Column(Date, nullable=False)
    hora_entrada = Column(Time, nullable=True)
    hora_salida = Column(Time, nullable=True)
    foto_entrada = Column(String(255), nullable=True)
    lat_entrada = Column(Numeric(10, 7), nullable=True)
    lng_entrada = Column(Numeric(10, 7), nullable=True)
    foto_salida = Column(String(255), nullable=True)
    lat_salida = Column(Numeric(10, 7), nullable=True)
    lng_salida = Column(Numeric(10, 7), nullable=True)
    estado = Column(String(20), nullable=False, default="Pendiente")
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
    )
    created_by = Column(Integer, ForeignKey("usuario.id"), nullable=True)
    updated_by = Column(Integer, ForeignKey("usuario.id"), nullable=True)

    trabajador = relationship("Trabajador")

    def __repr__(self):
        return f"<Asistencia {self.id}, trabajador={self.trabajador_id}, estado={self.estado}>"
    