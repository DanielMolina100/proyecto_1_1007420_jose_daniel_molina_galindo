import xml.etree.ElementTree as ET
from pathlib import Path

from src.archivos import leer_registros
from src.configuracion import cargar_configuracion


def exportar_a_xml():
    """
    Exporta todos los registros del archivo CSV a un archivo XML.
    """
    registros = leer_registros()

    if not registros:
        return False, "No existen registros para exportar."

    configuracion = cargar_configuracion()
    ruta_exportaciones = Path(
        configuracion["archivos"]["exportaciones"]
    )

    ruta_exportaciones.mkdir(parents=True, exist_ok=True)

    ruta_xml = ruta_exportaciones / "equipos.xml"

    raiz = ET.Element("equipos")

    for registro in registros:
        equipo_xml = ET.SubElement(raiz, "equipo")

        for campo, valor in registro.items():
            elemento = ET.SubElement(equipo_xml, campo)
            elemento.text = valor if valor is not None else ""

    arbol = ET.ElementTree(raiz)

    ET.indent(arbol, space="    ")

    arbol.write(
        ruta_xml,
        encoding="utf-8",
        xml_declaration=True
    )

    return True, f"Datos exportados correctamente a: {ruta_xml}"