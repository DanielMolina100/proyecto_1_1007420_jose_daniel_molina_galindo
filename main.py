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

from src.hashing import (
    construir_tabla_hash,
    buscar_por_hash
)

from src.integridad import (
    registrar_hashes,
    verificar_integridad
)

from src.logs import registrar_log
from src.pila import PilaOperaciones


pila_operaciones = PilaOperaciones()

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
        construir_tabla_hash()
        registrar_hashes()

    registrar_log(
        "CREACION",
        f"Se registro el equipo con ID {equipo['id']}."
    )
    
    pila_operaciones.push(
        f"Registro de equipo: {equipo['id']}"
    )

    print("Estructuras auxiliares e integridad actualizadas correctamente.")
    
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
    registrar_log(
        "BUSQUEDA",
        f"Busqueda secuencial del ID {id_equipo}. "
        f"Encontrado: {resultado['encontrado']}. "
        f"Registros recorridos: {resultado['registros_recorridos']}."
    )
    
    pila_operaciones.push(
        f"Busqueda secuencial: {id_equipo}"
    )
    
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
    registrar_log(
        "INDICE",
        f"Indice principal reconstruido. Registros indexados: {cantidad}."
    )
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
    registrar_log(
        "BUSQUEDA",
        f"Busqueda por indice del ID {id_equipo}. "
        f"Encontrado: {equipo is not None}."
    )
    
    pila_operaciones.push(
        f"Busqueda por indice: {id_equipo}"
    )
    
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
    registrar_log(
        "INDICE",
        f"Indice invertido reconstruido. Categorias indexadas: {cantidad}."
    )
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
    registrar_log(
        "BUSQUEDA",
        f"Busqueda por categoria '{categoria}'. "
        f"Resultados encontrados: {len(equipos)}."
    )
    
    pila_operaciones.push(
        f"Busqueda por categoria: {categoria}"
    )
    
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
    registrar_log(
        "INDICE",
        f"Indice multikey reconstruido. Combinaciones indexadas: {cantidad}."
    )
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
    registrar_log(
        "BUSQUEDA",
        f"Busqueda multikey. Departamento: {departamento}, "
        f"Estado: {estado}. Resultados: {len(equipos)}."
    )
    
    pila_operaciones.push(
        f"Busqueda multikey: {departamento} - {estado}"
    )
    
    print(f"\nDepartamento buscado: {departamento}")
    print(f"Estado buscado: {estado}")
    print(mensaje)

    if equipos:
        print("Resultado: ENCONTRADO")

        for equipo in equipos:
            mostrar_equipo(equipo)
    else:
        print("Resultado: NO ENCONTRADO")

def opcion_construir_tabla_hash():
    print("\n=== CONSTRUIR TABLA HASH ===")

    cantidad, colisiones, ruta = construir_tabla_hash()
    registrar_log(
        "HASHING",
        f"Tabla hash reconstruida. Registros: {cantidad}. "
        f"Colisiones: {colisiones}."
    )
    print("\nTabla hash construida correctamente.")
    print(f"Registros procesados: {cantidad}")
    print(f"Colisiones detectadas: {colisiones}")
    print(f"Archivo generado: {ruta}")

def opcion_buscar_por_hash():
    print("\n=== BUSQUEDA MEDIANTE HASHING ===")

    id_equipo = input("Ingrese el ID a buscar: ").strip()

    if not id_equipo:
        print("\nError: debe ingresar un ID.")
        return

    equipo, posicion, mensaje = buscar_por_hash(id_equipo)
    registrar_log(
        "BUSQUEDA",
        f"Busqueda mediante hashing del ID {id_equipo}. "
        f"Posicion hash: {posicion}. "
        f"Encontrado: {equipo is not None}."
    )
    
    pila_operaciones.push(
        f"Busqueda hashing: {id_equipo}"
    )
    
    print(f"\nID buscado: {id_equipo}")

    if posicion is not None:
        print(f"Posicion hash calculada: {posicion}")

    print(mensaje)

    if equipo:
        print("Resultado: ENCONTRADO")
        mostrar_equipo(equipo)
    else:
        print("Resultado: NO ENCONTRADO")

def opcion_registrar_hashes():
    print("\n=== REGISTRAR HUELLAS SHA-256 ===")

    cantidad, ruta = registrar_hashes()

    print("\nHuellas SHA-256 registradas correctamente.")
    print(f"Archivos registrados: {cantidad}")
    print(f"Archivo generado: {ruta}")
    registrar_log(
        "INTEGRIDAD",
        f"Se registraron huellas SHA-256 de {cantidad} archivos."
    )

def opcion_verificar_integridad():
    print("\n=== VERIFICAR INTEGRIDAD SHA-256 ===")

    resultado, detalles = verificar_integridad()

    if resultado is None:
        print("\nNo fue posible realizar la verificacion.")

        for mensaje in detalles:
            print(mensaje)

        return

    archivos_integros = 0
    archivos_alterados = 0

    print()

    for detalle in detalles:
        archivo = detalle["archivo"]
        estado = detalle["estado"]

        print(f"{archivo}: {estado}")

        if estado == "INTEGRO":
            archivos_integros += 1
        else:
            archivos_alterados += 1

    print("\nResumen de integridad:")
    print(f"Archivos integros: {archivos_integros}")
    print(f"Archivos con problemas: {archivos_alterados}")

    if archivos_alterados == 0:
        print("Resultado general: INTEGRIDAD CORRECTA")
    else:
        print("Resultado general: SE DETECTARON ALTERACIONES")
        
    registrar_log(
        "INTEGRIDAD",
        f"Verificacion realizada. Archivos integros: {archivos_integros}. "
        f"Archivos con problemas: {archivos_alterados}."
    )
    pila_operaciones.push(
        "Verificacion de integridad SHA-256"
    )
    
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
        construir_tabla_hash()
        registrar_hashes()
        registrar_log(
            "ACTUALIZACION",
            f"Se actualizo el equipo con ID {id_equipo}."
        )
        
    pila_operaciones.push(
        f"Actualizacion de equipo: {id_equipo}"
    )
        
    print("Estructuras auxiliares e integridad actualizadas correctamente.")

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
        construir_tabla_hash()
        registrar_hashes()
        registrar_log(
            "ELIMINACION",
            f"Se elimino el equipo con ID {id_equipo}."
        ) 
        pila_operaciones.push(
            f"Eliminacion de equipo: {id_equipo}"
        )         
        print("Estructuras auxiliares e integridad actualizadas correctamente.")
    else:
        print("\nEliminacion cancelada.")

def opcion_exportar_xml():
    print("\n=== EXPORTAR DATOS A XML ===")

    resultado, mensaje = exportar_a_xml()

    print(f"\n{mensaje}")
    registrar_log(
        "EXPORTACION",
        f"Exportacion XML ejecutada. Resultado: {mensaje}"
    )
    pila_operaciones.push(
        "Exportacion de datos a XML"
    )

def opcion_mostrar_historial_pila():
    print("\n=== HISTORIAL DE OPERACIONES - PILA LIFO ===")

    historial = pila_operaciones.obtener_historial()

    if not historial:
        print("\nLa pila de operaciones esta vacia.")
        return

    print(f"\nCantidad de operaciones almacenadas: {pila_operaciones.cantidad()}")
    print(f"TOP actual: {pila_operaciones.top()}")

    print("\nOperaciones desde el TOP:")

    for posicion, operacion in enumerate(historial, start=1):
        print(f"{posicion}. {operacion}")

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
    print("10. Construir/Reconstruir tabla hash")
    print("11. Busqueda mediante hashing")
    print("12. Registrar huellas SHA-256")
    print("13. Verificar integridad SHA-256")
    print("14. Actualizar equipo")
    print("15. Eliminar equipo")
    print("16. Exportar datos a XML")
    print("17. Ver historial de operaciones (Pila LIFO)")
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
            opcion_construir_tabla_hash()

        elif opcion == "11":
            opcion_buscar_por_hash()

        elif opcion == "12":
            opcion_registrar_hashes()

        elif opcion == "13":
            opcion_verificar_integridad()

        elif opcion == "14":
            opcion_actualizar()

        elif opcion == "15":
            opcion_eliminar()

        elif opcion == "16":
            opcion_exportar_xml()

        elif opcion == "17":
            opcion_mostrar_historial_pila()
        
        elif opcion == "0":
            print("\nPrograma finalizado.")
            break
        else:
            print("\nOpcion invalida. Intente nuevamente.")


if __name__ == "__main__":
    main()