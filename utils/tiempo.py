from datetime import datetime
from zoneinfo import ZoneInfo

ZONA_PERU = ZoneInfo("America/Lima")


def ahora():
    """Fecha y hora actual en la zona horaria de Perú,
    sin depender de la configuración del servidor."""
    return datetime.now(ZONA_PERU)