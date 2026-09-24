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
    print("\n=== BUSCAR EQUIPO POR ID ===")

    id_equipo = input("Ingrese el ID: ").strip()
    equipo = buscar_por_id(id_equipo)

    if equipo:
        mostrar_equipo(equipo)
    else:
        print("\nNo se encontro un equipo con ese ID.")


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
    print("3. Buscar equipo por ID")
    print("4. Actualizar equipo")
    print("5. Eliminar equipo")
    print("6. Exportar datos a XML")
    print("0. Salir")
    print("============================================")


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
            opcion_actualizar()

        elif opcion == "5":
            opcion_eliminar()

        elif opcion == "6":
            opcion_exportar_xml()
        
        elif opcion == "0":
            print("\nPrograma finalizado.")
            break

        else:
            print("\nOpcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()