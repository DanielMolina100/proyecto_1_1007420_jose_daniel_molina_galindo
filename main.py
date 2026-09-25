from src.archivos import (
    inicializar_archivo,
    registrar_equipo,
    leer_registros,
    buscar_por_id,
    actualizar_equipo,
    eliminar_equipo
)
from src.configuracion import obtener_datos_sistema
from src.exportacion import exportar_a_xml
from src.busquedas import busqueda_secuencial_por_id
from src.busquedas import busqueda_secuencial_por_id

from src.indices import (
    construir_indice_principal,
    buscar_por_indice,
    construir_indice_invertido,
    buscar_por_categoria,
    construir_indice_multikey,
    buscar_multikey
)


def mostrar_equipo(equipo):
    print("\n------------------------------")
    print(f"ID:           {equipo['id']}")
    print(f"Nombre:       {equipo['nombre']}")
    print(f"Categoria:    {equipo['categoria']}")
    print(f"Marca:        {equipo['marca']}")
    print(f"Modelo:       {equipo['modelo']}")
    print(f"Departamento: {equipo['departamento']}")
    print(f"Estado:       {equipo['estado']}")
    print(f"Fecha:        {equipo['fecha_registro']}")
    print("------------------------------")


def opcion_registrar():
    print("\n=== REGISTRAR EQUIPO ===")

    equipo = {
        "id": input("ID: ").strip(),
        "nombre": input("Nombre: ").strip(),
        "categoria": input("Categoria: ").strip(),
        "marca": input("Marca: ").strip(),
        "modelo": input("Modelo: ").strip(),
        "departamento": input("Departamento: ").strip(),
        "estado": input("Estado: ").strip(),
        "fecha_registro": ""
    }

    if not all([
        equipo["id"],
        equipo["nombre"],
        equipo["categoria"],
        equipo["marca"],
        equipo["modelo"],
        equipo["departamento"],
        equipo["estado"]
    ]):
        print("\nError: todos los campos son obligatorios.")
        return

    resultado, mensaje = registrar_equipo(equipo)
    print(f"\n{mensaje}")

    if resultado:
        construir_indice_principal()
        construir_indice_invertido()
        construir_indice_multikey()
    print("Indices actualizados correctamente.")

def opcion_consultar_todos():
    print("\n=== EQUIPOS REGISTRADOS ===")

    registros = leer_registros()

    if not registros:
        print("No existen equipos registrados.")
        return

    for equipo in registros:
        mostrar_equipo(equipo)

    print(f"\nTotal de equipos: {len(registros)}")


def opcion_buscar():
    print("\n=== BUSQUEDA SECUENCIAL POR ID ===")

    id_equipo = input("Ingrese el ID a buscar: ").strip()

    if not id_equipo:
        print("\nError: debe ingresar un ID.")
        return

    resultado = busqueda_secuencial_por_id(id_equipo)

    print("\n--- RESULTADO DE LA BUSQUEDA ---")
    print(f"Valor buscado: {resultado['valor_buscado']}")
    print(
        f"Registros recorridos: "
        f"{resultado['registros_recorridos']}"
    )

    if resultado["encontrado"]:
        print("Resultado: ENCONTRADO")
        mostrar_equipo(resultado["registro"])
    else:
        print("Resultado: NO ENCONTRADO")

def opcion_construir_indice():
    print("\n=== CONSTRUIR INDICE PRINCIPAL ===")

    cantidad, ruta = construir_indice_principal()

    print("\nIndice principal construido correctamente.")
    print(f"Registros indexados: {cantidad}")
    print(f"Archivo generado: {ruta}")

def opcion_buscar_por_indice():
    print("\n=== BUSQUEDA POR INDICE ===")

    id_equipo = input("Ingrese el ID a buscar: ").strip()

    if not id_equipo:
        print("\nError: debe ingresar un ID.")
        return

    equipo, mensaje = buscar_por_indice(id_equipo)

    print(f"\nValor buscado: {id_equipo}")
    print(mensaje)

    if equipo:
        print("Resultado: ENCONTRADO")
        mostrar_equipo(equipo)
    else:
        print("Resultado: NO ENCONTRADO")

def opcion_construir_indice_invertido():
    print("\n=== CONSTRUIR INDICE INVERTIDO ===")

    cantidad, ruta = construir_indice_invertido()

    print("\nIndice invertido construido correctamente.")
    print(f"Categorias indexadas: {cantidad}")
    print(f"Archivo generado: {ruta}")


def opcion_buscar_por_categoria():
    print("\n=== BUSQUEDA POR CATEGORIA ===")

    categoria = input("Ingrese la categoria a buscar: ").strip()

    if not categoria:
        print("\nError: debe ingresar una categoria.")
        return

    equipos, mensaje = buscar_por_categoria(categoria)

    print(f"\nCategoria buscada: {categoria}")
    print(mensaje)

    if equipos:
        print("Resultado: ENCONTRADO")

        for equipo in equipos:
            mostrar_equipo(equipo)
    else:
        print("Resultado: NO ENCONTRADO")

def opcion_construir_indice_multikey():
    print("\n=== CONSTRUIR INDICE MULTIKEY ===")

    cantidad, ruta = construir_indice_multikey()

    print("\nIndice multikey construido correctamente.")
    print(f"Combinaciones indexadas: {cantidad}")
    print(f"Archivo generado: {ruta}")

def opcion_buscar_multikey():
    print("\n=== BUSQUEDA MULTIKEY ===")

    departamento = input("Ingrese el departamento: ").strip()
    estado = input("Ingrese el estado: ").strip()

    if not departamento or not estado:
        print("\nError: departamento y estado son obligatorios.")
        return

    equipos, mensaje = buscar_multikey(departamento, estado)

    print(f"\nDepartamento buscado: {departamento}")
    print(f"Estado buscado: {estado}")
    print(mensaje)

    if equipos:
        print("Resultado: ENCONTRADO")

        for equipo in equipos:
            mostrar_equipo(equipo)
    else:
        print("Resultado: NO ENCONTRADO")

def opcion_actualizar():
    print("\n=== ACTUALIZAR EQUIPO ===")

    id_equipo = input("Ingrese el ID del equipo: ").strip()
    equipo = buscar_por_id(id_equipo)

    if not equipo:
        print("\nNo se encontro un equipo con ese ID.")
        return

    mostrar_equipo(equipo)

    print("\nIngrese los nuevos datos.")
    print("Presione ENTER para conservar el valor actual.\n")

    nuevos_datos = {}

    campos = [
        "nombre",
        "categoria",
        "marca",
        "modelo",
        "departamento",
        "estado"
    ]

    for campo in campos:
        nuevo_valor = input(
            f"{campo.capitalize()} [{equipo[campo]}]: "
        ).strip()

        if nuevo_valor:
            nuevos_datos[campo] = nuevo_valor

    resultado, mensaje = actualizar_equipo(id_equipo, nuevos_datos)
    print(f"\n{mensaje}")

    if resultado:
        construir_indice_principal()
        construir_indice_invertido()
        construir_indice_multikey()
    print("Indices actualizados correctamente.")


def opcion_eliminar():
    print("\n=== ELIMINAR EQUIPO ===")

    id_equipo = input("Ingrese el ID del equipo: ").strip()
    equipo = buscar_por_id(id_equipo)

    if not equipo:
        print("\nNo se encontro un equipo con ese ID.")
        return

    mostrar_equipo(equipo)

    confirmacion = input(
        "\n¿Esta seguro de eliminar este equipo? (S/N): "
    ).strip().lower()

    if confirmacion == "s":
            resultado, mensaje = eliminar_equipo(id_equipo)
    print(f"\n{mensaje}")

    if resultado:
        construir_indice_principal()
        construir_indice_invertido()
        construir_indice_multikey()
        print("Indices actualizados correctamente.")
    else:
        print("\nEliminacion cancelada.")

def opcion_exportar_xml():
    print("\n=== EXPORTAR DATOS A XML ===")

    resultado, mensaje = exportar_a_xml()

    print(f"\n{mensaje}")

def mostrar_menu():
    datos_sistema = obtener_datos_sistema()

    print("\n============================================")
    print(f" {datos_sistema['nombre'].upper()}")
    print(
        f" Version {datos_sistema['version']} | "
        f"Carne: {datos_sistema['carne']}"
    )
    print("============================================")
    print("1. Registrar equipo")
    print("2. Consultar todos los equipos")
    print("3. Busqueda secuencial por ID")
    print("4. Construir/Reconstruir indice principal")
    print("5. Busqueda por indice")
    print("6. Construir/Reconstruir indice invertido")
    print("7. Busqueda por categoria")
    print("8. Construir/Reconstruir indice multikey")
    print("9. Busqueda multikey")
    print("10. Actualizar equipo")
    print("11. Eliminar equipo")
    print("12. Exportar datos a XML")
    print("0. Salir")

def main():
    inicializar_archivo()

    while True:
        mostrar_menu()

        opcion = input("Seleccione una opcion: ").strip()

        if opcion == "1":
            opcion_registrar()

        elif opcion == "2":
            opcion_consultar_todos()

        elif opcion == "3":
            opcion_buscar()

        elif opcion == "4":
            opcion_construir_indice()

        elif opcion == "5":
            opcion_buscar_por_indice()

        elif opcion == "6":
            opcion_construir_indice_invertido()

        elif opcion == "7":
            opcion_buscar_por_categoria()

        elif opcion == "8":
            opcion_construir_indice_multikey()

        elif opcion == "9":
            opcion_buscar_multikey()

        elif opcion == "10":
            opcion_actualizar()

        elif opcion == "11":
            opcion_eliminar()

        elif opcion == "12":
            opcion_exportar_xml()

        elif opcion == "0":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nOpcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()