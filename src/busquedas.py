from src.archivos import leer_registros


def busqueda_secuencial_por_id(id_buscado):
    """
    Realiza una busqueda secuencial por ID.

    Recorre los registros uno por uno hasta encontrar
    el identificador solicitado o llegar al final.
    """

    registros = leer_registros()
    recorridos = 0

    for registro in registros:
        recorridos += 1

        if registro["id"].lower() == id_buscado.lower():
            return {
                "encontrado": True,
                "valor_buscado": id_buscado,
                "registro": registro,
                "registros_recorridos": recorridos
            }

    return {
        "encontrado": False,
        "valor_buscado": id_buscado,
        "registro": None,
        "registros_recorridos": recorridos
    }