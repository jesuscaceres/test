import json
import csv
from datetime import datetime

# Precio en dólares
PRECIO_BOTELLA = 15
PRECIO_VASO = 8
# Peso en gramos
PESO_BOTELLA = 450
PESO_VASO = 350


def cargar_pedidos() -> dict:
    """Lee un archivo con extensión .csv para cargar los pedidos en un diccionario en memoria

    Returns:
        dict: Un diccionario representando la estructura de los pedidos
    """
    with open('csv/pedidos.csv', newline='', encoding='utf-8') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        lista_pedidos = list(lector)

        pedidos_archivo: dict = {}
        for indice in range(1, len(lista_pedidos)):
            registro_actual: list = lista_pedidos[indice]
            nro_pedido: str = registro_actual[0]
            if nro_pedido not in pedidos_archivo.keys():
                pedidos_archivo[nro_pedido]: dict = {
                    "fecha": registro_actual[1],
                    "cliente": registro_actual[2],
                    "ciudad": str(registro_actual[3]),
                    "provincia": str(registro_actual[4]),
                    "productos": {
                        registro_actual[5]: {
                            str(registro_actual[6]).lower(): {
                                "cantidad": int(registro_actual[7])
                            }
                        }
                    },
                    "descuento": float(registro_actual[8]),
                    "enviado": False
                }
            else:
                productos: dict = pedidos_archivo[str(nro_pedido)]["productos"]
                codigo: str = registro_actual[5]
                if codigo in productos.keys():
                    items: dict = productos[codigo]
                    items[str(registro_actual[6]).lower()] = {
                        "cantidad": int(registro_actual[7])
                    }
                else:
                    productos[codigo] = {
                        str(registro_actual[6]).lower(): {
                            "cantidad": int(registro_actual[7])
                        }
                    }
        return pedidos_archivo


def leer_opcion(opciones: list[str]) -> str:
    """Muestra las posibles opciones y lee la opción ingresada por el usuario.

    Args:
        opciones (list[str]): La lista de opciones posibles.

    Returns:
        str: La opción elegida.
    """
    print('')
    for i, opcion in enumerate(opciones):
        print(f"\t{i + 1}. {opcion}")
    return input('\n\t\tIngrese su opción: ')


def obtener_valor_positivo(campo: str) -> int:
    """Le pide un valor entero positivo al usuario. Si este es incorrecto, pide ingresar nuevamente.

    Args:
         campo (str): La etiqueta del campo a ser solicitado.

    Returns:
        int: El valor ingresado.
    """
    valor: int = 0
    while not valor > 0:
        try:
            valor = int(input(f"\n\t[*] {campo}: "))
            if valor <= 0:
                raise ValueError
        except ValueError:
            print("\n\tValor incorrecto. Debe ingresar un número entero positivo.")
    return valor


def obtener_valor_en_rango(campo: str, inicio: int, fin: int) -> float:
    """Le pide un valor al usuario que esté dentro de determinado rango. Si este es incorrecto, pide ingresar nuevamente.

    Args:
         campo (str): La etiqueta del campo a ser solicitado.
         inicio (int): Valor inicial del rango
         fin (int): Valor tope del rango

    Returns:
        float: El valor ingresado.
    """
    valor: float = -1
    while not (0 <= valor <= 100):
        try:
            valor = float(input(f"\n\t[*] {campo}: "))
            if valor < inicio or valor > fin:
                raise ValueError
        except ValueError:
            print("\n\tValor incorrecto. Debe ingresar un valor entre 0 y 100 (inclusive).")
    return valor


def obtener_opciones_validas(lista: list[str]) -> list[str]:
    """Devuelve la lista de posibles opciones validas

    Args:
        lista (list[str]): Posibles opciones

    Returns:
        list[str]: Lista de posibles opciones. Ej: ["1", "2", "3"]
    """
    return list(map(lambda x: str(x), list(range(1, len(lista) + 1))))


def obtener_color_valido(opcion_articulo: str) -> str:
    """Le pide al usuario un color de acuerdo al tipo de articulo. Si no es válido, pide ingresar nuevamente.

    Args:
        opcion_articulo (str): Tipo de artículo elegido. 1: Botella, 2: Vasos

    Returns:
        str: El color elegido.
    """
    colores_botella: list[str] = ["Verde", "Rojo", "Azul", "Negro", "Amarillo"]
    colores_vaso: list[str] = ["Negro", "Azul"]
    opcion_color: str = ''
    color: str = ''
    if opcion_articulo == "1":
        opciones_validas: list[str] = obtener_opciones_validas(colores_botella)
        while opcion_color not in opciones_validas:
            opcion_color = leer_opcion(colores_botella)
            if opcion_color in opciones_validas:
                color = colores_botella[int(opcion_color) - 1].lower()
            else:
                print("\n\tIngrese una opción válida.")
    else:
        opciones_validas: list[str] = obtener_opciones_validas(colores_vaso)
        while opcion_color not in opciones_validas:
            opcion_color = leer_opcion(colores_vaso)
            if opcion_color in opciones_validas:
                color = colores_vaso[int(opcion_color) - 1].lower()
            else:
                print("\n\tIngrese una opción válida.")
    return color


def obtener_articulo_valido() -> (str, str):
    """Le pide al usuario que ingrese el tipo de articulo que desea.
    1. Botella
    2. Vaso

    Returns:
          (str, str): El código del artículo y la opción elegida.
    """
    opcion_articulo: str = ''
    codigo: str = ''
    print("\n\t<<< Lista de artículos >>>")
    while opcion_articulo not in ["1", "2"]:
        opcion_articulo = leer_opcion(["Botella", "Vaso"])
        if opcion_articulo == '1':
            codigo = '1334'
        elif opcion_articulo == '2':
            codigo = '568'
        else:
            print('\n\tIngrese una opción válida.')
    return codigo, opcion_articulo


def obtener_fecha_valida() -> str:
    """Le pide al usuario que ingrese una fecha válida según el formato dd/mm/yyyy.
    Si no es válida, pide ingresar nuevamente la fecha.

    Returns:
        str: La fecha ingresada.
    """
    fecha_valida: bool = False
    fecha: str = ''
    while not fecha_valida:
        fecha = input("\n\t[*] Fecha: ")
        formato: str = "%d/%m/%Y"
        try:
            fecha_valida = bool(datetime.strptime(fecha, formato))
        except ValueError:
            print("\n\t\tIngrese una fecha válida. Debe respetar el formato dd/mm/yyyy")
            fecha_valida = False
    return fecha


def agregar_nuevos_articulos(productos: dict) -> None:
    """Permite agregar contínuamente artículos.

    Args:
          productos (dict): Diccionario que contiene la información de productos: código, color y cantidad.
    """
    opcion: str = ''
    while opcion != 'N':
        codigo, opcion_articulo = obtener_articulo_valido()
        color = obtener_color_valido(opcion_articulo)
        cantidad = obtener_valor_positivo("Cantidad")

        if codigo not in productos.keys():
            productos[codigo] = {
                color: {
                    "cantidad": cantidad
                }
            }
        else:
            items: dict = productos[codigo]
            if color not in items.keys():
                items[color] = {
                    "cantidad": cantidad
                }
            else:
                print(
                    f"\n\t\tPara el artículo cod-{codigo} ya fue ingresado el color {color}. Si desea, después puede modificar el pedido.")
        opcion = input("\n\tDesea agregar otro artículo? [S/N]  ").upper()


def cargar_productos() -> dict:
    """Permite ingresar continuamente artículos hasta que el usuario lo indique.

    Returns:
        dict: Un diccionario que representa la cantidad de productos ingresados por color.
    """
    productos: dict = {}
    agregar_nuevos_articulos(productos)
    return productos


def crear_pedido(_pedidos: dict) -> None:
    """Permite dar de alta un nuevo pedido.

    Args:
        _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
    """
    fecha: str = obtener_fecha_valida()
    cliente: str = input("\n\t[*] Cliente: ")
    ciudad: str = input("\n\t[*] Ciudad: ")
    provincia: str = input("\n\t[*] Provincia: ")
    productos: dict = cargar_productos()
    descuento: float = obtener_valor_en_rango("Descuento", 0, 100)

    nro_pedido = len(_pedidos) + 1
    _pedidos[str(nro_pedido)] = {
        "fecha": fecha,
        "cliente": cliente,
        "ciudad": ciudad,
        "provincia": provincia,
        "productos": productos,
        "descuento": descuento,
        "enviado": False
    }
    print("\n\t\tNuevo pedido agregado correctamente.")


def modificar_campo(_dict: dict, key: str, campo: str) -> None:
    """Permite modificar un campo específico de un pedido.

    Args:
        _dict (dict): Diccionario que contiene la estructura base de los pedidos.
        key (str): Clave de la propiedad a modificar.
        campo (str): Propiedad a modificar
    """
    print(f"\n\t\tValor anterior: {_dict[key][campo]}")
    if campo == "fecha":
        nuevo_valor = obtener_fecha_valida()
    elif campo == "cantidad":
        nuevo_valor = obtener_valor_positivo("Cantidad")
    elif campo == "descuento":
        nuevo_valor = obtener_valor_en_rango("Descuento", 0, 100)
    else:
        nuevo_valor = input("\n\t\tNuevo valor: ")
    _dict[key][campo] = nuevo_valor


def eliminar_color(colores: dict, id_articulo: str) -> None:
    """Permite eliminar un color de la lista de articulos cargados.

    Args:
        colores (dict): Diccionario de articulos por colores.
        id_articulo (str): Define de qué articulo se trata, botella o vaso.
    """
    color: str = obtener_color_valido(id_articulo)
    if color in colores.keys():
        del colores[color]
        print(f"\n\t\tSe eliminó el color {color}.")
    else:
        print("\n\t\tNo existe un artículo con ese color.")


def modificar_color(colores: dict, id_articulo: str) -> None:
    """Permite modificar un color de la lista de articulos cargados.

    Args:
        colores (dict): Diccionario de articulos por colores.
        id_articulo (str): Define de qué articulo se trata, botella o vaso.
    """
    color: str = obtener_color_valido(id_articulo)
    if color in colores.keys():
        opcion_campo = ''
        while opcion_campo != '2':
            opcion_campo = leer_opcion(["Cantidad", "Salir"])
            if opcion_campo == '1':
                modificar_campo(colores, color, "cantidad")
            elif opcion_campo == '2':
                continue
            else:
                print("\n\n\t\tIngrese una opción válida.")
    else:
        print("\n\t\tNo existe un artículo con ese color.")


def agregar_color(colores: dict, id_articulo: str) -> None:
    """Permite agregar un nuevo color a la lista de articulos cargados.

    Args:
        colores (dict): Diccionario de articulos por colores.
        id_articulo (str): Define de qué articulo se trata, botella o vaso.
    """
    color: str = obtener_color_valido(id_articulo)
    if color in colores.keys():
        print("\n\t\tYa existe este color.")
    else:
        cantidad: int = obtener_valor_positivo("Cantidad")
        colores[color] = {
            "cantidad": cantidad
        }


def modificar_propiedades_articulos(productos: dict) -> None:
    """Permite modificar las propiedades de un articulo particular: color y cantidad.

    Args:
        productos (dict): Diccionario con la información de los artículos actualmente cargados.
    """
    codigo: str = input("\n\tIngrese el código del producto a modificar: ")
    if codigo in productos.keys():
        id_articulo: str = "1" if codigo == "1334" else "2"
        opcion: str = ''
        colores: dict = productos[codigo]
        while opcion != '4':
            opcion = leer_opcion(["Nuevo color", "Modificar color", "Eliminar color", "Salir"])
            if opcion == '1':
                agregar_color(colores, id_articulo)
            elif opcion == '2':
                modificar_color(colores, id_articulo)
            elif opcion == '3':
                eliminar_color(colores, id_articulo)
            elif opcion == '4':
                continue
            else:
                print("\n\t\tIngrese una opción válida.")
    else:
        print("\n\t\tNo existe un artículo con ese código.")


def modificar_articulos(_pedidos: dict, nro_pedido: str) -> None:
    """Muestra los artículos actuales para determinado pedido con la posibilidad de modificarlos.

    Args:
        _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
        nro_pedido (str): Identificador del pedido
    """
    accion: str = ''
    while accion != '4':
        accion = leer_opcion(["Agregar artículo", "Modificar artículo", "Eliminar articulo", "Salir"])
        print("\n\t\tArtículos actuales: ")
        productos: dict = _pedidos[nro_pedido]['productos']
        print(json.dumps(productos, indent=4, ensure_ascii=False))
        if accion == '1':
            agregar_nuevos_articulos(productos)
        elif accion == '2':
            modificar_propiedades_articulos(productos)
        elif accion == '3':
            codigo, _ = obtener_articulo_valido()
            if codigo in productos.keys():
                del productos[codigo]
                print(f"\n\t\tSe eliminó el artículo {codigo}.")
            else:
                print("\n\t\tNo existe un artículo con ese código.")


def modificar_pedido(_pedidos: dict) -> None:
    """Permite modificar un pedido existente.

    Args:
        _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
    """
    if len(_pedidos) > 0:
        print("\n\t\tPedidos actuales:", end=' ')
        lista_nro_pedidos: list[str] = []
        for key in _pedidos.keys():
            if not _pedidos[key]["enviado"]:
                lista_nro_pedidos.append(key)
        print(", ".join(f"[{nro}]" for nro in lista_nro_pedidos))
        nro_pedido = input("\n\tIngrese el número de pedido a modificar: ")
        if nro_pedido in _pedidos.keys():
            opcion_modificar = ''
            while opcion_modificar != '7':
                opcion_modificar = leer_opcion(
                    ["Fecha", "Cliente", "Ciudad", "Provincia", "Productos", "Descuento", "Salir"])
                if opcion_modificar == '1':
                    modificar_campo(_pedidos, nro_pedido, "fecha")
                elif opcion_modificar == '2':
                    modificar_campo(_pedidos, nro_pedido, "cliente")
                elif opcion_modificar == '3':
                    modificar_campo(_pedidos, nro_pedido, "ciudad")
                elif opcion_modificar == '4':
                    modificar_campo(_pedidos, nro_pedido, "provincia")
                elif opcion_modificar == '5':
                    modificar_articulos(_pedidos, nro_pedido)
                elif opcion_modificar == '6':
                    modificar_campo(_pedidos, nro_pedido, "descuento")
        else:
            print("\n\t\tNo existe ningún pedido con ese número.")
    else:
        print("\n\t\tNo hay pedidos cargados actualmente.")


def eliminar_pedido(_pedidos: dict) -> None:
    """Permite eliminar un pedido ingresando el número.

    Args:
        _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
    """
    print("\n\t\tPedidos actuales:", end=' ')
    lista_nro_pedidos: list[str] = []
    for key in _pedidos.keys():
        if not _pedidos[key]["enviado"]:
            lista_nro_pedidos.append(key)
    print(", ".join(f"[{nro}]" for nro in lista_nro_pedidos))
    nro_pedido = input("\n\t\tIngrese el número de órden a eliminar: ")
    if nro_pedido in _pedidos.keys():
        del _pedidos[nro_pedido]
    else:
        print("\n\tNo existe ningún pedido con ese número.")


def listar_pedidos(_pedidos: dict) -> None:
    """Permite listar los pedidos que se encuentran cargados actualmente.

    Args:
        _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
    """
    if len(_pedidos) > 0:
        print(json.dumps(_pedidos, indent=4, ensure_ascii=False))
    else:
        print("\n\t\tNo existen pedidos cargados actualmente.")


def pedidos_abm(_pedidos: dict) -> None:
    """Muestra un menú que permite el alta, baja y modificación de pedidos.

    Args:
        _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
    """
    opcion: str = ''
    while opcion != '5':
        opcion = leer_opcion(["Crear pedido", "Modificar pedido", "Eliminar pedido", "Listar pedidos", "Salir"])
        if opcion == '1':
            crear_pedido(_pedidos)
        elif opcion == '2':
            modificar_pedido(_pedidos)
        elif opcion == '3':
            eliminar_pedido(_pedidos)
        elif opcion == '4':
            listar_pedidos(_pedidos)
        elif opcion == '5':
            print('')
        else:
            print("\n\t\t'Por favor, ingrese una opción válida.")


def imprimir_total(articulos_enviados: dict, ciudad: str) -> None:
    """Imprime por pantalla el coste total de los artículos enviados a determinada ciudad.

    Args:
        articulos_enviados (dict): Diccionario con los articulos enviados detallando cantidad y costos.
        ciudad (str): Ciudad dónde fueron enviados los artículos.
    """
    if len(articulos_enviados) > 0:
        print(f"\n\t\t\tSe enviaron los siguientes artículos a la ciudad de '{ciudad}':")
        for key in articulos_enviados.keys():
            precio = PRECIO_BOTELLA if key == "1334" else PRECIO_VASO
            if key == "568":
                print(f"\n\t\t({articulos_enviados[key]['cantidad']}) vasos x ${precio} usd c/u")
            else:
                print(f"\n\t\t({articulos_enviados[key]['cantidad']}) botellas x ${precio} usd c/u")
            print(f"\t\tSubtotal --- ${articulos_enviados[key]['bruto']} usd")
            print(f"\t\tDescuento -- {articulos_enviados[key]['descuento']}%")
            print(f"\t\t{'-' * 30}")
            print(f"\t\tTOTAL ------ ${articulos_enviados[key]['neto']} usd")
    else:
        print(f"\n\t\tNo se ha envíado ningún artículo a {ciudad}.")


def obtener_valor_total_por_ciudad(_pedidos: dict, ciudad: str) -> None:
    """Permite conocer el valor total de los articulos enviados a determinada ciudad.

    Args:
         _pedidos (dict): Diccionario que contiene la estructura base de los pedidos.
         ciudad (str): Ciudad dónde fueron enviados los artículos.
    """
    articulos_enviados: dict = {}
    for k1 in _pedidos.keys():
        if _pedidos[k1]["enviado"] and (_pedidos[k1]["ciudad"].upper() == ciudad.upper()):
            productos: dict = _pedidos[k1]["productos"]
            descuento: float = _pedidos[k1]["descuento"]
            for k2 in productos.keys():
                colores: dict = productos[k2]
                precio: float = PRECIO_BOTELLA if k2 == "1334" else PRECIO_VASO
                for k3 in colores.keys():
                    cantidad: int = colores[k3]["cantidad"]
                    if k2 not in articulos_enviados.keys():
                        articulos_enviados[k2] = {
                            "cantidad": cantidad,
                            "descuento": descuento,
                            "bruto": float(precio * cantidad),
                            "neto": (precio * cantidad) * (100 - descuento) / 100
                        }
                    else:
                        item = articulos_enviados[k2]
                        item["cantidad"] += cantidad
                        item["bruto"] += float(precio * cantidad)
                        item["neto"] += (precio * cantidad) * (100 - descuento) / 100

    imprimir_total(articulos_enviados, ciudad)


# Prueba de ejecución
pedidos = cargar_pedidos()
pedidos_abm(pedidos)
