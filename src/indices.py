import json
from pathlib import Path

from src.archivos import leer_registros
from src.configuracion import cargar_configuracion


def obtener_ruta_indice():
    configuracion = cargar_configuracion()
    carpeta_indices = Path(configuracion["archivos"]["indices"])
    carpeta_indices.mkdir(parents=True, exist_ok=True)
    return carpeta_indices / "indice_principal.json"


def construir_indice_principal():
    """
    Construye un indice que relaciona cada ID
    con su posicion dentro del archivo CSV.
    """
    registros = leer_registros()
    indice = {}

    for posicion, registro in enumerate(registros):
        indice[registro["id"].upper()] = posicion

    ruta_indice = obtener_ruta_indice()

    with open(ruta_indice, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, indent=4, ensure_ascii=False)

    return len(indice), ruta_indice


def cargar_indice_principal():
    """
    Carga el indice principal almacenado en JSON.
    """
    ruta_indice = obtener_ruta_indice()

    if not ruta_indice.exists():
        return None

    try:
        with open(ruta_indice, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return None


def buscar_por_indice(id_buscado):
    """
    Busca un ID en el indice y recupera su registro
    utilizando la posicion almacenada.
    """
    indice = cargar_indice_principal()

    if indice is None:
        return None, "El indice no existe o tiene un formato invalido."

    id_normalizado = id_buscado.upper()

    if id_normalizado not in indice:
        return None, "El ID no existe en el indice."

    posicion = indice[id_normalizado]
    registros = leer_registros()

    if not isinstance(posicion, int) or not 0 <= posicion < len(registros):
        return None, "El indice esta desactualizado. Debe reconstruirse."

    registro = registros[posicion]

    if registro["id"].upper() != id_normalizado:
        return None, "El indice esta desactualizado. Debe reconstruirse."

    return registro, f"Registro localizado mediante el indice en la posicion {posicion}."