# administrador_de_tienda.py
#
# Jorge Claudio González Becerril A01412375
# Juan Daniel Rodríguez Oropeza A01411625
# 10/2020

# Definición de funciones


def editar_matriz_suma(matriz, fila, columna, valor_a_sumar):
    ''' Regresa una matriz con un valor alterado por una suma. '''

    matriz[fila][columna] = str(int(matriz[fila][columna]) + valor_a_sumar)


def mostrar_lista_en_menu(lista):
    ''' Muestra al usuario una lista desplegada. '''

    print('')
    i = 1
    for nombre in lista:
        print(f"{i}) {nombre}")
        i += 1


def obtener_columna(matriz, tipo_de_columna):
    ''' Regresa la columna de una matriz en forma de lista. '''

    columna = []

    for fila in matriz:
        columna.append(fila[tipo_de_columna])

    return columna


def obtener_diccionario_columnas_ventas():
    ''' Regresa un diccionario de las columnas en el archivo de texto de ventas. '''

    diccionario = {"id": 0}
    texto_ventas = open("ventas.txt", "r")
    linea = texto_ventas.readline()
    texto_ventas.close()

    linea = linea.split("\t")

    # Por cada producto que hay agrega una llave al diccionario
    for i in range(1,len(linea)):
        diccionario[f"producto {i - 1}"] = i  # {"producto n": n + 1"}

    return diccionario


def pasar_texto_a_matriz(nombre_texto):
    ''' Regresa una matriz apartir de un archivo de texto. '''

    matriz = []
    texto = open(nombre_texto, "r")

    # Elimina los \n y convierte las lineas en listas usando \t de separador
    for linea in texto:
        linea = linea.replace("\n", "")
        matriz.append(linea.split("\t"))

    texto.close()

    return matriz


def pasar_matriz_a_texto(nombre_texto, matriz):
    ''' Crea o modifica un archivo de texto apartir de una matriz. '''

    # Junta en una sola cadena toda la matriz, utilizando \t como separador entre columnas y \n entre filas
    cadena_de_matriz = '\n'.join('\t'.join(columnas) for columnas in matriz)

    texto = open(nombre_texto, "w")
    texto.write(cadena_de_matriz)
    texto.close()


def pedir_entero(num_min, num_max='infinito', peticion=''):
    ''' Regresa un entero cuando se encuentra dentro de un rango específico. '''

    while True:
        # Solo acepta números enteros
        try:
            numero = int(input(f"\n{peticion} >> "))
        except:
            print("Ingrese un número válido.")
            continue

        # Solo acepta números entre los rangos establecidos.
        # Si no hay valor máximo, se asume que es infinito.
        if num_min <= numero:
            if num_max == 'infinito':
                return numero
            elif numero <= num_max:
                return numero

        print("Ingrese un número valido.")


def pedir_eleccion(matriz, tipo_de_columna, peticion):
    ''' Muestra al usuario una lista de opciones y regresa su eleccion en un entero. '''

    # Obtiene la lista de opciones a desplegar
    lista = obtener_columna(matriz, tipo_de_columna)
    cantidad_lista = len(lista)
    mostrar_lista_en_menu(lista)

    eleccion = pedir_entero(1, cantidad_lista, f"{peticion} (1-{cantidad_lista})")

    return eleccion


# Funciones de Menús


def mostrar_menu():
    ''' Muestra al usuario el menú principal del programa. '''

    print(f"\n1) Registrar ventas\n"
          f"2) Registrar llegada de artículos al almacén\n"
          f"3) Consultar datos del inventario\n"
          f"4) Consultar datos de las ventas\n"
          f"5) Mostrar reportes de ventas por vendedor\n"
          f"6) Mostrar reportes de ventas por artículo\n"
          f"7) Cerrar")


def mostrar_menu_registrar_ventas():
    '''
    Despliega el menú 1.
    Permite a un vendedor registar la venta de un producto por su parte.
    '''

    eleccion_vendedor = pedir_eleccion(matriz_vendedores, columnas_vendedores.get("nombre"), "Seleccione su nombre")
    id_vendedor = eleccion_vendedor - 1

    eleccion_producto = pedir_eleccion(matriz_inventario, columnas_inventario.get("nombre"),
                                       "Seleccione el producto a vender")
    id_producto = eleccion_producto - 1

    # Obtiene la cantidad disponible del producto
    cantidad = obtener_columna(matriz_inventario, columnas_inventario.get("cantidad"))
    cantidad_producto = int(cantidad[id_producto])

    # Avisa si el producto se encuentra agotado
    if cantidad_producto < 1:
        print("\nEl producto se encuentra agotado.")
        input("Da click para continuar.")
        return

    eleccion_cantidad = pedir_entero(1, cantidad_producto, f"Cantidad del producto a vender (1-{cantidad_producto})")

    # Actualiza los cambios realizados en las matrices
    editar_matriz_suma(matriz_ventas, id_vendedor, id_producto + 1, eleccion_cantidad)
    editar_matriz_suma(matriz_inventario, id_producto, columnas_inventario.get("cantidad"), -eleccion_cantidad)


def mostrar_menu_registrar_llegada():
    '''
    Despliega el menú 2.
    Permite registrar la llegada de productos para abastecer el inventario.
    '''

    eleccion_producto = pedir_eleccion(matriz_inventario, columnas_inventario.get("nombre"), "Seleccione el producto que llegó")
    id_producto = eleccion_producto - 1

    cantidad_producto = pedir_entero(1, peticion="Cantidad abastecida del producto")

    # Actualiza los cambios realizados en las matrices
    editar_matriz_suma(matriz_inventario, id_producto, columnas_inventario.get("cantidad"), cantidad_producto)


def mostrar_menu_consultar_inventario():
    '''
    Despliega el menú 3.
    Permite consultar la cantidad disponible de un producto en específico.
    '''

    cantidad_productos = len(matriz_inventario)

    # Imprime al usuario todos los productos con sus cantidades disponibles.
    for producto in range(cantidad_productos):
        nombre_producto = matriz_inventario[producto][columnas_inventario.get("nombre")]
        cantidad_producto = matriz_inventario[producto][columnas_inventario.get("cantidad")]

        print(f"\n{nombre_producto}\n"
              f">> {cantidad_producto} unidades restantes.")

    input("\nDa Enter para continuar.")


def mostrar_menu_consultar_ventas():
    '''
    Despliega el menú 4.
    Permite consultar la cantidad de ventas realizadas de un producto en específico.
    '''

    cantidad_productos = len(matriz_inventario)

    # Imprime al usuario todos los productos con sus ventas totales.
    for producto in range(cantidad_productos):
        nombre_producto = matriz_inventario[producto][columnas_inventario.get("nombre")]
        venta_producto = 0
        
        # Suma todas las ventas parciales del producto
        for vendedor in matriz_ventas:
            cantidad_venta = vendedor[columnas_ventas.get(f"producto {str(producto)}")]
            venta_producto += int(cantidad_venta)

        print(f"\n{nombre_producto}\n"
              f">> {venta_producto} ventas totales.")

    input("\nDa Enter para continuar.")


def mostrar_menu_reporte_vendedor():
    '''
    Despliega el menú 5.
    Permite revisar un reporte de los productos vendidos por cada vendedor.
    '''

    eleccion_vendedor = pedir_eleccion(matriz_vendedores, columnas_vendedores.get("nombre"), "Seleccione el vendedor")
    id_vendedor = eleccion_vendedor - 1
    nombre_vendedor = matriz_vendedores[id_vendedor][columnas_vendedores.get("nombre")]

    print(f"\n| Reporte de Ventas de {nombre_vendedor} |\n")

    # Imprime todos los productos, con las cantidades vendidas por el vendedor a un lado
    for productos in range(len(matriz_inventario)):
        producto = matriz_inventario[productos][columnas_inventario.get("nombre")]
        vendidos = matriz_ventas[id_vendedor][productos + 1]

        print(f"{producto} >> {vendidos} vendidos.")

    input("\nDa Enter para continuar.")


def mostrar_menu_reporte_producto():
    '''
    Despliega el menú 6.
    Permite revisar un reporte de la cantidad de veces que un producto se ha vendido por cada vendedor.
    '''

    eleccion_producto = pedir_eleccion(matriz_inventario, columnas_inventario.get("nombre"), "Seleccione el producto")
    id_producto = eleccion_producto - 1
    nombre_producto = matriz_inventario[id_producto][columnas_inventario.get("nombre")]

    print(f"\n| Reporte de Ventas de {nombre_producto} |\n")

    # Imprime todos los vendedores, con las cantidades que vendieron del producto a un lado
    for vendedores in range(len(matriz_vendedores)):
        vendedor = matriz_vendedores[vendedores][columnas_vendedores.get("nombre")]
        vendidos = matriz_ventas[vendedores][id_producto + 1]

        print(f"{vendedor} >> {vendidos} vendidos.")

    input("\nDa Enter para continuar.")


# Declaración de diccionarios

columnas_inventario = {"id": 0, "nombre": 1, "cantidad": 2}
columnas_vendedores = {"id": 0, "nombre": 1}
columnas_ventas = obtener_diccionario_columnas_ventas()  # {"id": 0, "producto 0": 1, ..., "producto n": n + 1}

# Declaración de matrices

matriz_inventario = pasar_texto_a_matriz("inventario.txt")
matriz_vendedores = pasar_texto_a_matriz("vendedores.txt")
matriz_ventas = pasar_texto_a_matriz("ventas.txt")

# Main

print("Bienvenido al Administrador de Tienda")

while True:
    mostrar_menu()
    eleccion = pedir_entero(1, 7, "Seleccione un menú (1-7)")

    if eleccion == 1:
        mostrar_menu_registrar_ventas()
    elif eleccion == 2:
        mostrar_menu_registrar_llegada()
    elif eleccion == 3:
        mostrar_menu_consultar_inventario()
    elif eleccion == 4:
        mostrar_menu_consultar_ventas()
    elif eleccion == 5:
        mostrar_menu_reporte_vendedor()
    elif eleccion == 6:
        mostrar_menu_reporte_producto()
    elif eleccion == 7:
        pasar_matriz_a_texto("inventario.txt", matriz_inventario)
        pasar_matriz_a_texto("ventas.txt", matriz_ventas)
        break