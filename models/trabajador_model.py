class Trabajador:

    def __init__(self, id, dni, nombres, apellidos, cargo, estado=1):
        self.id        = id
        self.dni       = dni
        self.nombres   = nombres
        self.apellidos = apellidos
        self.cargo     = cargo
        self.estado    = estado

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def __repr__(self):
        return f"Trabajador({self.id}, {self.dni}, {self.nombre_completo()}, {self.cargo})"
    
    