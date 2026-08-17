class Usuario:

    def __init__(self, id, nombre, usuario, password, rol="supervisor", estado=1):
        self.id       = id
        self.nombre   = nombre
        self.usuario  = usuario
        self.password = password
        self.rol      = rol
        self.estado   = estado

        