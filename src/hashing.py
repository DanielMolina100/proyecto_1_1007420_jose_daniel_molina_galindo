import json
from pathlib import Path

from src.archivos import leer_registros
from src.configuracion import cargar_configuracion


TAMANO_TABLA = 7


def obtener_ruta_tabla_hash():
    configuracion = cargar_configuracion()
    carpeta_indices = Path(configuracion["archivos"]["indices"])
    carpeta_indices.mkdir(parents=True, exist_ok=True)

    return carpeta_indices / "tabla_hash.json"


def calcular_hash(clave):
    """
    Calcula una posicion mediante una funcion hash polinomial.

    Formula:
    hash = (hash * 31 + codigo_ascii) % TAMANO_TABLA
    """
    valor_hash = 0

    for caracter in clave.upper():
        valor_hash = (
            valor_hash * 31 + ord(caracter)
        ) % TAMANO_TABLA

    return valor_hash


def construir_tabla_hash():
    """
    Construye una tabla hash utilizando el ID como clave.
    Las colisiones se resuelven mediante encadenamiento.
    """
    registros = leer_registros()

    tabla = {
        str(posicion): []
        for posicion in range(TAMANO_TABLA)
    }

    colisiones = 0

    for registro in registros:
        id_equipo = registro["id"].upper()
        posicion = calcular_hash(id_equipo)

        if len(tabla[str(posicion)]) > 0:
            colisiones += 1

        tabla[str(posicion)].append({
            "id": id_equipo,
            "posicion_csv": registros.index(registro)
        })

    ruta_tabla = obtener_ruta_tabla_hash()

    with open(ruta_tabla, "w", encoding="utf-8") as archivo:
        json.dump(
            tabla,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    return len(registros), colisiones, ruta_tabla


def cargar_tabla_hash():
    """
    Carga la tabla hash almacenada en formato JSON.
    """
    ruta_tabla = obtener_ruta_tabla_hash()

    if not ruta_tabla.exists():
        return None

    try:
        with open(ruta_tabla, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return None


def buscar_por_hash(id_buscado):
    """
    Localiza un equipo utilizando su ID y la tabla hash.
    """
    tabla = cargar_tabla_hash()

    if tabla is None:
        return None, None, (
            "La tabla hash no existe o tiene un formato invalido."
        )

    id_normalizado = id_buscado.upper()
    posicion_hash = calcular_hash(id_normalizado)

    cubeta = tabla.get(str(posicion_hash), [])

    for elemento in cubeta:
        if elemento["id"] == id_normalizado:
            registros = leer_registros()
            posicion_csv = elemento["posicion_csv"]

            if 0 <= posicion_csv < len(registros):
                registro = registros[posicion_csv]

                if registro["id"].upper() == id_normalizado:
                    return (
                        registro,
                        posicion_hash,
                        "Registro localizado mediante hashing."
                    )

            return (
                None,
                posicion_hash,
                "La tabla hash esta desactualizada."
            )

    return (
        None,
        posicion_hash,
        "El ID no fue encontrado en la tabla hash."
    )