import shutil
from datetime import datetime
from pathlib import Path

from src.configuracion import cargar_configuracion


def obtener_carpeta_backups():
    """
    Obtiene la carpeta principal donde se almacenan
    los respaldos del sistema.
    """
    configuracion = cargar_configuracion()
    carpeta = Path(configuracion["archivos"]["respaldos"])

    carpeta.mkdir(parents=True, exist_ok=True)

    return carpeta


def obtener_archivos_para_backup():
    """
    Retorna los archivos necesarios para recuperar
    el estado del sistema.
    """
    return [
        Path("data/registros.csv"),
        Path("config/configuracion.json"),
        Path("indices/indice_principal.json"),
        Path("indices/indice_invertido_categoria.json"),
        Path("indices/indice_multikey.json"),
        Path("indices/tabla_hash.json"),
        Path("indices/hashes.json"),
    ]

def crear_backup():            
    
    """
    Crea un respaldo en una carpeta identificada
    mediante fecha y hora.
    """
    carpeta_backups = obtener_carpeta_backups()

    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    carpeta_backup = carpeta_backups / f"backup_{fecha_hora}"

    try:
        carpeta_backup.mkdir(parents=True, exist_ok=False)

        archivos_copiados = 0

        for ruta_origen in obtener_archivos_para_backup():
            if not ruta_origen.exists():
                continue

            ruta_destino = carpeta_backup / ruta_origen

            ruta_destino.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(ruta_origen, ruta_destino)
            archivos_copiados += 1

        return True, carpeta_backup, archivos_copiados

    except OSError as error:
        if carpeta_backup.exists():
            shutil.rmtree(
                carpeta_backup,
                ignore_errors=True
            )

        return False, str(error), 0

def listar_backups():
    """
    Obtiene los respaldos disponibles ordenados
    desde el mas reciente al mas antiguo.
    """
    carpeta_backups = obtener_carpeta_backups()

    backups = [
        carpeta
        for carpeta in carpeta_backups.iterdir()
        if carpeta.is_dir()
        and carpeta.name.startswith("backup_")
    ]

    backups.sort(
        key=lambda carpeta: carpeta.name,
        reverse=True
    )

    return backups

def restaurar_backup(nombre_backup):
    """
    Restaura los archivos almacenados en un backup
    seleccionado por el usuario.
    """
    carpeta_backups = obtener_carpeta_backups()
    carpeta_backup = carpeta_backups / nombre_backup

    if not carpeta_backup.exists():
        return False, "El backup seleccionado no existe."

    if not carpeta_backup.is_dir():
        return False, "La ruta seleccionada no corresponde a un backup."

    archivos_restaurados = 0

    try:
        for ruta_origen in carpeta_backup.rglob("*"):
            if not ruta_origen.is_file():
                continue

            ruta_relativa = ruta_origen.relative_to(carpeta_backup)
            ruta_destino = Path(ruta_relativa)

            ruta_destino.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            shutil.copy2(
                ruta_origen,
                ruta_destino
            )

            archivos_restaurados += 1

        return (
            True,
            f"Backup restaurado correctamente. "
            f"Archivos restaurados: {archivos_restaurados}."
        )

    except OSError as error:
        return (
            False,
            f"Error durante la restauracion: {error}"
        )