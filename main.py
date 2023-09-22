import Tree as util
import pandas as pd

resA = None
resB = []

dataframe = pd.read_csv('co_properties_final.csv')
tree = util.AVLTree()

for indice, fila in dataframe.iterrows():
    title = fila['title']
    department = fila['department']
    city = fila['city']
    property_type = fila['property_type']
    latitude = fila['latitude']
    longitude = fila['longitude']
    surface_total = fila['surface_total']
    surface_covered = fila['surface_covered']
    bedrooms = fila['bedrooms']
    bathrooms = fila['bathrooms']
    operation_type = fila['operation_type']
    price = fila['price']
    tree.insert_node(title, department, city, property_type, latitude, longitude, surface_total, surface_covered, bedrooms, bathrooms, operation_type, price,"white")
def insertar_nodo_1():
    price = float(input("Ingrese el precio: "))
    surface_total = float(input("Ingrese el total de la superficie: "))
    found_node = tree.search_node(price, surface_total)
    if found_node:
        print("Ya existe un nodo con esta metrica!")
    else:
        title = input("Ingrese el titulo: ")
        department = input("Ingrese el departamento: ")
        city = input("Ingrese la ciudad: ")
        property_type = input("Ingrese el tipo de propiedad: ")
        latitude = float(input("Ingrese la latitud: "))
        longitude = float(input("Ingrese la longitud: "))
        surface_covered = float(input("Ingrese el total de la superficie cubierta: "))
        bedrooms = int(input("Ingrese el numero de habitaciones: "))
        bathrooms = int(input("Ingrese el numero de baños: "))
        operation_type = input("Ingrese el tipo de operation: ")
        tree.insert_node(title, department, city, property_type, latitude, longitude, surface_total, surface_covered,
                         bedrooms, bathrooms, operation_type, price,"green")
        print("El nodo fue insertado exitosamente!")
        tree.generar_imagen()
        tree.abrir_imagen()
        found_node = tree.search_node(price, surface_total)
        found_node.color = "white"

def eliminar_nodo_2():
    price_to_delete = float(input("Ingrese el precio para calcular la metrica: "))
    surface_total_to_delete = float(input("Ingrese el la superficie total para calcular la metrica: "))
    print(f"La metrica es de {price_to_delete/surface_total_to_delete:.1f}, buscando nodo....")
    found_node = tree.search_node(price_to_delete, surface_total_to_delete)
    if found_node:
        tree.delete_node(price_to_delete, surface_total_to_delete)
        print("El nodo fue eliminado exitosamente!")
        tree.generar_imagen()
        tree.abrir_imagen()
    else:
        print("No fue encontrado ningún nodo con esta metrica!")

def buscar_nodo_3():
    price_to_delete = float(input("Ingrese el precio para calcular la metrica: "))
    surface_total_to_delete = float(input("Ingrese el la superficie total para calcular la metrica: "))
    print(f"La metrica es de {price_to_delete / surface_total_to_delete:.1f}, buscando nodo....")
    found_node = tree.search_node(price_to_delete, surface_total_to_delete)
    if found_node:
        resA = found_node
        print("El nodo fue encontrado exitosamente!")
        found_node.color = "yellow"
        tree.generar_imagen()
        tree.abrir_imagen()
        found_node.color = "white"
    else:
        print("No fue encontrado ningún nodo con esta metrica!")

def buscar_nodos_4():
    city = input("¿A que ciudad deben pertenecer los nodos? ")
    cuartos = int(input("¿Cual es el minimo numero de cuartos que deben tener los nodos? "))
    precio = float(input("¿Cual el precio minimo que deben tener los nodos? "))
    print(f"Buscando nodos pertenecientes a {city}, con un numero de cuartos mayor a {cuartos} y un precio minimo de {precio}:")
    result = tree.search_nodes_by_criteria(city,cuartos,precio)
    if result:
        resB.clear()
        for nodo in result:
            resB.append(nodo)
            nodo.color = "yellow"
        tree.generar_imagen()
        tree.abrir_imagen()
        for nodo in result:
            nodo.color = "white"
    else:
        print("No se encontraron nodos con el criterio elegido!")

def recorrer_por_niveles_5():
    resultados_por_niveles = tree.recorrido_por_niveles()
    if resultados_por_niveles:
        print("Recorrido por niveles del árbol:")
        for nivel, nodos in enumerate(resultados_por_niveles, start=1):
            print(f"Nivel {nivel}:")
            for nodo in nodos:
                print(f"    Título: {nodo.title}")

def mostrar_informacion_6(nodos):
    if nodos:
        size = len(nodos)
        while True:
            target = int(input(f"Por favor eliga una numero del 1 al {size} para seleccionar un nodo: "))
            if target < 1 or target > size:
                print(f"El numero no es valido!")
            else:
                selected = nodos[target-1]
                print("El nodo fue seleccionado correctamente!")
                acceder_menu_2(selected)
                break
    else:
        print("Primero use las opciones 4 o 5")

def acceder_menu_2(nodo):
    while True:
        mostrar_menu_2()
        opcion2 = input("Selecciona una opción: ")
        if opcion2 == "1":
            print(f"El nivel del nodo es: {tree.get_node_level(nodo)}")
        elif opcion2 == "2":
            print(f"El factor de balanceo del nodo es: {tree.balance_factor(nodo)}")
        elif opcion2 == "3":
            padre = tree.find_parent(nodo)
            if padre is not None:
                nodo.color = "gray"
                padre.color = "yellow"
                tree.generar_imagen()
                tree.abrir_imagen()
                nodo.color = "white"
                padre.color = "white"
            else:
                print("El nodo seleccionado no tiene nodo padre")
        elif opcion2 == "4":
            abuelo = tree.find_grandparent(nodo)
            if abuelo is not None:
                nodo.color = "gray"
                abuelo.color = "yellow"
                tree.generar_imagen()
                tree.abrir_imagen()
                nodo.color = "white"
                abuelo.color = "white"
            else:
                print("El nodo seleccionado no tiene nodo abuelo")
        elif opcion2 == "5":
            tio = tree.find_uncle(nodo)
            if tio is not None:
                nodo.color = "gray"
                tio.color = "yellow"
                tree.generar_imagen()
                tree.abrir_imagen()
                nodo.color = "white"
                tio.color = "white"
            else:
                print("El nodo seleccionado no tiene nodo tio")
        elif opcion2 == '6':
            break
        else:
            print("Opción no válida. Por favor, elige una opción válida.")


def mostrar_menu():
    print("===========[ARBOL AVL]===========")
    print("1. Insertar nodo")
    print("2. Eliminar nodo utilizando metrica")
    print("3. Buscar nodo utilizando metrica")
    print("4. Buscar nodos siguiendo criterio")
    print("5. Mostrar recorrido por niveles")
    print("6. Mostrar información de un nodo")
    print("7. Mostrar arbol")
    print("8. Salir")
    print("=================================")

def mostrar_menu_2():
    print("===========[INFORMACIÓN NODO]===========")
    print("1. Obtener nivel del nodo")
    print("2. Obtener factor de balanceo del nodo")
    print("3. Encontrar padre del nodo")
    print("4. Encontrar el abuelo del nodo")
    print("5. Encontrar el tio del nodo")
    print("6. Atras")
    print("=================================")

# Bucle principal del programa
while True:
    mostrar_menu()
    opcion = input("Selecciona una opción: ")
    if opcion == "1":
        insertar_nodo_1()
    elif opcion == "2":
        eliminar_nodo_2()
    elif opcion == "3":
        buscar_nodo_3()
    elif opcion == "4":
        buscar_nodos_4()
    elif opcion == "5":
        recorrer_por_niveles_5()
    elif opcion == "6":
        nodos = []
        if resA is not None:
            nodos.append(resA)
        if resB:
            for no in resB:
                nodos.append(no)
        mostrar_informacion_6(nodos)
    elif opcion == '7':
        tree.generar_imagen()
        tree.abrir_imagen()
    elif opcion == '8':
        print("Hasta luego!!!!")
        break
    else:
        print("Opción no válida. Por favor, elige una opción válida.")