from datetime import datetime
from pathlib import Path

from src.configuracion import cargar_configuracion


def obtener_ruta_log():
    """
    Obtiene la ruta del archivo de log definida
    en la configuracion general del sistema.
    """
    configuracion = cargar_configuracion()
    ruta_log = Path(configuracion["archivos"]["logs"])

    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    return ruta_log


def registrar_log(tipo, descripcion):
    """
    Registra un evento del sistema incluyendo
    fecha, hora, tipo de operacion y descripcion.
    """
    ruta_log = obtener_ruta_log()

    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    linea = (
        f"[{fecha_hora}] "
        f"[{tipo.upper()}] "
        f"{descripcion}\n"
    )

    try:
        with open(ruta_log, "a", encoding="utf-8") as archivo:
            archivo.write(linea)

        return True

    except OSError:
        return False


def leer_logs():
    """
    Lee todos los eventos almacenados
    en el archivo de log.
    """
    ruta_log = obtener_ruta_log()

    if not ruta_log.exists():
        return []

    try:
        with open(ruta_log, "r", encoding="utf-8") as archivo:
            return archivo.readlines()

    except OSError:
        return []