import csv
from datetime import datetime

from src.configuracion import (
    obtener_ruta_principal,
    obtener_configuracion_general
)


RUTA_ARCHIVO = obtener_ruta_principal()

CAMPOS = [
    "id",
    "nombre",
    "categoria",
    "marca",
    "modelo",
    "departamento",
    "estado",
    "fecha_registro"
]


def inicializar_archivo():
    """
    Crea el archivo principal CSV si no existe.
    """
    RUTA_ARCHIVO.parent.mkdir(parents=True, exist_ok=True)

    if not RUTA_ARCHIVO.exists():
        with open(RUTA_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
            escritor.writeheader()


def leer_registros():
    """
    Lee todos los registros almacenados en el archivo CSV.
    Maneja archivo inexistente, vacio o con formato invalido.
    """
    if not RUTA_ARCHIVO.exists():
        print(
            f"\nError: no se encontro el archivo principal "
            f"{RUTA_ARCHIVO}."
        )
        return []

    try:
        if RUTA_ARCHIVO.stat().st_size == 0:
            print(
                f"\nError: el archivo principal "
                f"{RUTA_ARCHIVO} esta vacio."
            )
            return []

        registros = []

        with open(
            RUTA_ARCHIVO,
            "r",
            newline="",
            encoding="utf-8"
        ) as archivo:
            lector = csv.DictReader(archivo)

            if lector.fieldnames is None:
                print(
                    "\nError: el archivo CSV no contiene "
                    "encabezados validos."
                )
                return []

            if lector.fieldnames != CAMPOS:
                print(
                    "\nError: el archivo CSV no tiene "
                    "el formato esperado."
                )
                return []

            for registro in lector:
                registros.append(registro)

        return registros

    except (OSError, csv.Error) as error:
        print(
            f"\nError al leer el archivo principal: {error}"
        )
        return []


def existe_id(id_equipo):
    """
    Verifica si un identificador ya existe.
    """
    registros = leer_registros()

    for registro in registros:
        if registro["id"].lower() == id_equipo.lower():
            return True

    return False


def registrar_equipo(equipo):
    """
    Agrega un nuevo equipo al archivo CSV.
    """
    inicializar_archivo()

    if existe_id(equipo["id"]):
        return False, "El ID ingresado ya existe."

    configuracion = obtener_configuracion_general()
    formato_fecha = configuracion["formato_fecha"]

    equipo["fecha_registro"] = datetime.now().strftime(formato_fecha)       

    with open(RUTA_ARCHIVO, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writerow(equipo)

    return True, "Equipo registrado correctamente."


def buscar_por_id(id_equipo):
    """
    Busca un equipo por su identificador.
    """
    registros = leer_registros()

    for registro in registros:
        if registro["id"].lower() == id_equipo.lower():
            return registro

    return None


def actualizar_equipo(id_equipo, nuevos_datos):
    """
    Modifica los datos de un equipo existente.
    """
    registros = leer_registros()
    encontrado = False

    for registro in registros:
        if registro["id"].lower() == id_equipo.lower():
            for campo, valor in nuevos_datos.items():
                if campo in CAMPOS and campo not in ("id", "fecha_registro"):
                    registro[campo] = valor

            encontrado = True
            break

    if not encontrado:
        return False, "No existe un equipo con ese ID."

    with open(RUTA_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(registros)

    return True, "Equipo actualizado correctamente."


def eliminar_equipo(id_equipo):
    """
    Elimina un equipo del archivo CSV.
    """
    registros = leer_registros()

    nuevos_registros = [
        registro
        for registro in registros
        if registro["id"].lower() != id_equipo.lower()
    ]

    if len(registros) == len(nuevos_registros):
        return False, "No existe un equipo con ese ID."

    with open(RUTA_ARCHIVO, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(nuevos_registros)

    return True, "Equipo eliminado correctamente."