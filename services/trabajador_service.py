from flask import session
from datetime import date

from config.extensions import db
from models.trabajador import Trabajador
from sqlalchemy.exc import IntegrityError


class TrabajadorService:

    def listar(self):
        return (
            Trabajador.query.filter_by(estado=True).order_by(Trabajador.apellidos).all()
        )

    def listar_inactivos(self):
        return (
            Trabajador.query.filter_by(estado=False)
            .order_by(Trabajador.apellidos)
            .all()
        )

    def buscar_por_dni(self, dni):
        return Trabajador.query.filter_by(dni=dni, estado=True).first()

    def crear(self, trabajador):
        db.session.add(trabajador)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception(
                f"Ya existe un trabajador registrado con el DNI {trabajador.dni}"
            )
        return trabajador.id

    def actualizar(self, trabajador):
        existente = Trabajador.query.get(trabajador.id)
        if not existente:
            raise Exception("Trabajador no encontrado")
        existente.dni = trabajador.dni
        existente.nombres = trabajador.nombres
        existente.apellidos = trabajador.apellidos
        existente.cargo = trabajador.cargo
        existente.fecha_nac = trabajador.fecha_nac
        existente.fecha_ingreso = trabajador.fecha_ingreso
        existente.fecha_cese = trabajador.fecha_cese
        existente.updated_by = session.get("usuario_id")

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise Exception(f"El DNI {trabajador.dni} ya pertenece a otro trabajador")

    def eliminar(self, id):
        trabajador = Trabajador.query.get(id)
        if not trabajador:
            raise Exception("Trabajador no encontrado")
        trabajador.estado = False
        trabajador.fecha_cese = trabajador.fecha_cese or date.today()
        trabajador.updated_by = session.get("usuario_id")
        db.session.commit()

    def reactivar(self, id):
        trabajador = Trabajador.query.get(id)
        if not trabajador:
            raise Exception("Trabajador no encontrado")
        trabajador.estado = True
        trabajador.fecha_cese = None
        db.session.commit()
