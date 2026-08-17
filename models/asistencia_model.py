class Asistencia:

    def __init__(self, id, trabajador_id, obra, fecha, hora_entrada, hora_salida,
                 cargo=None,
                 foto_entrada=None, lat_entrada=None, lng_entrada=None,
                 foto_salida=None, lat_salida=None, lng_salida=None,
                 estado='Pendiente'):
        self.id            = id
        self.trabajador_id = trabajador_id
        self.obra          = obra
        self.fecha         = fecha
        self.hora_entrada  = hora_entrada
        self.hora_salida   = hora_salida
        self.cargo         = cargo
        self.foto_entrada  = foto_entrada
        self.lat_entrada   = lat_entrada
        self.lng_entrada   = lng_entrada
        self.foto_salida   = foto_salida
        self.lat_salida    = lat_salida
        self.lng_salida    = lng_salida
        self.estado        = estado

    def __repr__(self):
        return f"Asistencia({self.id}, trabajador={self.trabajador_id}, {self.fecha}, {self.estado})"
    