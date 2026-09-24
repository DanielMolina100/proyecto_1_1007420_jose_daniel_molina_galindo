import json
from pathlib import Path


RUTA_CONFIGURACION = Path("config/configuracion.json")


def cargar_configuracion():
    """
    Carga la configuracion general del sistema desde un archivo JSON.
    """
    if not RUTA_CONFIGURACION.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de configuracion: "
            f"{RUTA_CONFIGURACION}"
        )

    try:
        with open(RUTA_CONFIGURACION, "r", encoding="utf-8") as archivo:
            configuracion = json.load(archivo)

        return configuracion

    except json.JSONDecodeError as error:
        raise ValueError(
            f"El archivo de configuracion JSON no tiene un formato valido: "
            f"{error}"
        )


def obtener_ruta_principal():
    configuracion = cargar_configuracion()
    return Path(configuracion["archivos"]["principal"])


def obtener_datos_sistema():
    configuracion = cargar_configuracion()
    return configuracion["sistema"]


def obtener_configuracion_general():
    configuracion = cargar_configuracion()
    return configuracion["configuracion"]