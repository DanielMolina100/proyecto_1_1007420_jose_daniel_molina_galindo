import os
from datetime import datetime
from pathlib import Path


def obtener_metadatos(ruta_archivo):
    """
    Obtiene metadatos reales de un archivo del sistema.
    """
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        return None

    if not ruta.is_file():
        return None

    try:
        estadisticas = ruta.stat()

        metadatos = {
            "nombre": ruta.name,
            "ruta": str(ruta),
            "extension": ruta.suffix if ruta.suffix else "Sin extension",
            "tamano_bytes": estadisticas.st_size,
            "fecha_creacion": datetime.fromtimestamp(
                estadisticas.st_ctime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_modificacion": datetime.fromtimestamp(
                estadisticas.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S"),
            "lectura": os.access(ruta, os.R_OK),
            "escritura": os.access(ruta, os.W_OK)
        }

        return metadatos

    except OSError:
        return None