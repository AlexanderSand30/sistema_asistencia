import mysql.connector
from mysql.connector import Error
import logging
import os
from dotenv import load_dotenv

load_dotenv()

CARPETA_LOGS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(CARPETA_LOGS, exist_ok=True)
RUTA_LOG = os.path.join(CARPETA_LOGS, "errores.log")

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(RUTA_LOG),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def obtener_conexion():
    """Establece conexión con la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host     = os.getenv("DB_HOST", "localhost"),
            user     = os.getenv("DB_USER", "root"),
            password = os.getenv("DB_PASSWORD", ""),
            database = os.getenv("DB_NAME", ""),
            charset  = "utf8mb4"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        logger.error(f"Error de conexión: {str(e)}")
        raise


if __name__ == "__main__":
    conexion = obtener_conexion()
    if conexion:
        print("✅ Conexión exitosa a la base de datos")
        conexion.close()

        