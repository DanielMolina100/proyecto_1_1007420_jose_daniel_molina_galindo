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

def obtener_ruta_indice_invertido():
    configuracion = cargar_configuracion()
    carpeta_indices = Path(configuracion["archivos"]["indices"])
    carpeta_indices.mkdir(parents=True, exist_ok=True)

    return carpeta_indices / "indice_invertido_categoria.json"


def construir_indice_invertido():
    """
    Construye un indice invertido utilizando la categoria
    de los equipos como clave y los ID como referencias.
    """
    registros = leer_registros()
    indice_invertido = {}

    for registro in registros:
        categoria = registro["categoria"].strip()
        id_equipo = registro["id"].upper()

        if categoria not in indice_invertido:
            indice_invertido[categoria] = []

        indice_invertido[categoria].append(id_equipo)

    ruta_indice = obtener_ruta_indice_invertido()

    with open(ruta_indice, "w", encoding="utf-8") as archivo:
        json.dump(
            indice_invertido,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    return len(indice_invertido), ruta_indice


def cargar_indice_invertido():
    """
    Carga desde disco el indice invertido por categoria.
    """
    ruta_indice = obtener_ruta_indice_invertido()

    if not ruta_indice.exists():
        return None

    try:
        with open(ruta_indice, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return None


def buscar_por_categoria(categoria_buscada):
    """
    Busca los equipos pertenecientes a una categoria
    utilizando el indice invertido.
    """
    indice = cargar_indice_invertido()

    if indice is None:
        return [], "El indice invertido no existe o es invalido."

    categoria_encontrada = None

    for categoria in indice:
        if categoria.lower() == categoria_buscada.lower():
            categoria_encontrada = categoria
            break

    if categoria_encontrada is None:
        return [], "La categoria no existe en el indice invertido."

    ids = indice[categoria_encontrada]
    registros = leer_registros()

    equipos_encontrados = []

    for registro in registros:
        if registro["id"].upper() in ids:
            equipos_encontrados.append(registro)

    return (
        equipos_encontrados,
        f"Se encontraron {len(equipos_encontrados)} equipo(s) "
        f"en la categoria '{categoria_encontrada}'."
    )
    
def obtener_ruta_indice_multikey():
    configuracion = cargar_configuracion()
    carpeta_indices = Path(configuracion["archivos"]["indices"])
    carpeta_indices.mkdir(parents=True, exist_ok=True)

    return carpeta_indices / "indice_multikey.json"


def construir_indice_multikey():
    """
    Construye un indice multikey utilizando como clave
    la combinacion departamento + estado.
    """
    registros = leer_registros()
    indice_multikey = {}

    for registro in registros:
        departamento = registro["departamento"].strip()
        estado = registro["estado"].strip()

        clave = f"{departamento}|{estado}"
        id_equipo = registro["id"].upper()

        if clave not in indice_multikey:
            indice_multikey[clave] = []

        indice_multikey[clave].append(id_equipo)

    ruta_indice = obtener_ruta_indice_multikey()

    with open(ruta_indice, "w", encoding="utf-8") as archivo:
        json.dump(
            indice_multikey,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    return len(indice_multikey), ruta_indice


def cargar_indice_multikey():
    """
    Carga desde disco el indice multikey.
    """
    ruta_indice = obtener_ruta_indice_multikey()

    if not ruta_indice.exists():
        return None

    try:
        with open(ruta_indice, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return None


def buscar_multikey(departamento_buscado, estado_buscado):
    """
    Busca equipos mediante la combinacion
    departamento + estado.
    """
    indice = cargar_indice_multikey()

    if indice is None:
        return [], "El indice multikey no existe o es invalido."

    clave_encontrada = None

    for clave in indice:
        departamento, estado = clave.split("|", 1)

        if (
            departamento.lower() == departamento_buscado.lower()
            and estado.lower() == estado_buscado.lower()
        ):
            clave_encontrada = clave
            break

    if clave_encontrada is None:
        return [], (
            "No existen equipos con la combinacion "
            "de departamento y estado indicada."
        )

    ids = indice[clave_encontrada]
    registros = leer_registros()
    equipos_encontrados = []

    for registro in registros:
        if registro["id"].upper() in ids:
            equipos_encontrados.append(registro)

    return (
        equipos_encontrados,
        f"Se encontraron {len(equipos_encontrados)} equipo(s) "
        f"para la combinacion indicada."
    )