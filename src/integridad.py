import hashlib
import json
from pathlib import Path

from src.configuracion import cargar_configuracion


def obtener_ruta_hashes():
    configuracion = cargar_configuracion()
    carpeta_indices = Path(configuracion["archivos"]["indices"])
    carpeta_indices.mkdir(parents=True, exist_ok=True)

    return carpeta_indices / "hashes.json"


def calcular_sha256(ruta_archivo):
    """
    Calcula la huella SHA-256 de un archivo.
    """
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        return None

    sha256 = hashlib.sha256()

    try:
        with open(ruta, "rb") as archivo:
            while True:
                bloque = archivo.read(4096)

                if not bloque:
                    break

                sha256.update(bloque)

        return sha256.hexdigest()

    except OSError:
        return None


def obtener_archivos_integridad():
    """
    Obtiene los archivos relevantes que seran
    controlados mediante SHA-256.
    """
    configuracion = cargar_configuracion()

    return [
        Path(configuracion["archivos"]["principal"]),
        Path("config/configuracion.json"),
        Path("indices/indice_principal.json"),
        Path("indices/indice_invertido_categoria.json"),
        Path("indices/indice_multikey.json"),
        Path("indices/tabla_hash.json")
    ]


def registrar_hashes():
    """
    Calcula y almacena las huellas SHA-256
    de los archivos relevantes del sistema.
    """
    hashes = {}

    for ruta in obtener_archivos_integridad():
        huella = calcular_sha256(ruta)

        if huella is not None:
            hashes[str(ruta)] = huella

    ruta_hashes = obtener_ruta_hashes()

    with open(ruta_hashes, "w", encoding="utf-8") as archivo:
        json.dump(
            hashes,
            archivo,
            indent=4,
            ensure_ascii=False
        )

    return len(hashes), ruta_hashes


def verificar_integridad():
    """
    Compara las huellas actuales con las almacenadas
    previamente en hashes.json.
    """
    ruta_hashes = obtener_ruta_hashes()

    if not ruta_hashes.exists():
        return None, ["No existe un registro previo de hashes."]

    try:
        with open(ruta_hashes, "r", encoding="utf-8") as archivo:
            hashes_guardados = json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return None, ["El archivo hashes.json es invalido."]

    resultados = []

    for ruta_texto, hash_guardado in hashes_guardados.items():
        ruta = Path(ruta_texto)

        if not ruta.exists():
            resultados.append({
                "archivo": ruta_texto,
                "estado": "NO ENCONTRADO"
            })
            continue

        hash_actual = calcular_sha256(ruta)

        if hash_actual == hash_guardado:
            estado = "INTEGRO"
        else:
            estado = "MODIFICADO"

        resultados.append({
            "archivo": ruta_texto,
            "estado": estado
        })

    return True, resultados