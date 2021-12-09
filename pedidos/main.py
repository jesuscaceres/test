import json
import csv
from datetime import datetime

# Precio en dólares
PRECIO_BOTELLA = 15
PRECIO_VASO = 8
# Peso en gramos
PESO_BOTELLA = 450
PESO_VASO = 350


def cargar_pedidos():
    with open('csv/pedidos.csv', newline='', encoding='utf-8') as archivo_csv:
        lector = csv.reader(archivo_csv, delimiter=',')
        lista_pedidos = list(lector)

        pedidos_archivo = {}
        for indice in range(1, len(lista_pedidos)):
            registro_actual = lista_pedidos[indice]
            nro_pedido = registro_actual[0]
            if nro_pedido not in pedidos_archivo.keys():
                pedidos_archivo[nro_pedido] = {
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
                productos = pedidos_archivo[str(nro_pedido)]["productos"]
                codigo = registro_actual[5]
                if codigo in productos.keys():
                    items = productos[codigo]
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


def leer_opcion(opciones: list[str]):
    print('')
    for i, opcion in enumerate(opciones):
        print(f"\t{i + 1}. {opcion}")
    return input('\n\t\tIngrese su opción: ')


def obtener_valor_positivo(campo: str):
    valor = 0
    while not valor > 0:
        try:
            valor = int(input(f"\n\t[*] {campo}: "))
            if valor <= 0:
                raise ValueError
        except ValueError:
            print("\n\tValor incorrecto. Debe ingresar un número entero positivo.")
    return valor


def obtener_valor_en_rango(campo: str, inicio: int, fin: int):
    valor = -1
    while not (0 <= valor <= 100):
        try:
            valor = float(input(f"\n\t[*] {campo}: "))
            if valor < inicio or valor > fin:
                raise ValueError
        except ValueError:
            print("\n\tValor incorrecto. Debe ingresar un valor entre 0 y 100 (inclusive).")
    return valor


def obtener_opciones_validas(lista_colores: list[str]) -> list[str]:
    return list(map(lambda x: str(x), list(range(1, len(lista_colores) + 1))))


def obtener_color_valido(opcion_articulo):
    colores_botella: list[str] = ["Verde", "Rojo", "Azul", "Negro", "Amarillo"]
    colores_vaso: list[str] = ["Negro", "Azul"]
    opcion_color: str = ''
    color: str = ''
    if opcion_articulo == "1":
        opciones_validas = obtener_opciones_validas(colores_botella)
        while opcion_color not in opciones_validas:
            opcion_color = leer_opcion(colores_botella)
            if opcion_color in opciones_validas:
                color = colores_botella[int(opcion_color) - 1].lower()
            else:
                print("\n\tIngrese una opción válida.")
    else:
        opciones_validas = obtener_opciones_validas(colores_vaso)
        while opcion_color not in opciones_validas:
            opcion_color = leer_opcion(colores_vaso)
            if opcion_color in opciones_validas:
                color = colores_vaso[int(opcion_color) - 1].lower()
            else:
                print("\n\tIngrese una opción válida.")
    return color


def obtener_articulo_valido():
    opcion_articulo = ''
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


def obtener_fecha_valida():
    fecha_valida = False
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


def cargar_productos():
    productos: dict = {}
    opcion: str = ''
    while opcion != 'N':
        codigo, opcion_articulo = obtener_articulo_valido()
        color = obtener_color_valido(opcion_articulo)
        cantidad = obtener_valor_positivo("Cantidad")

        if codigo in productos.keys():
            items = productos[codigo]
            items[color] = {
                "cantidad": cantidad
            }
        else:
            productos[codigo] = {
                color: {
                    "cantidad": cantidad
                }
            }
        opcion = input("\n\tDesea agregar otro artículo? [S/N]  ").upper()
    return productos


def crear_pedido(_pedidos: dict):
    fecha = obtener_fecha_valida()
    cliente: str = input("\n\t[*] Cliente: ")
    ciudad: str = input("\n\t[*] Ciudad: ")
    provincia: str = input("\n\t[*] Provincia: ")
    productos = cargar_productos()
    descuento = obtener_valor_en_rango("Descuento", 0, 100)

    nro_pedido = len(_pedidos) + 1
    _pedidos[str(nro_pedido)] = {
        "fecha": fecha,
        "cliente": cliente,
        "ciudad": ciudad,
        "provincia": provincia,
        "productos": productos,
        "descuento": descuento
    }
    print("\n\t\tNuevo pedido agregado correctamente.")


def modificar_campo(_dict, key, campo):
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


def eliminar_color(colores, id_articulo):
    color = obtener_color_valido(id_articulo)
    if color in colores.keys():
        del colores[color]
        print(f"\n\t\tSe eliminó el color {color}.")
    else:
        print("\n\t\tNo existe un artículo con ese color.")


def modificar_color(colores, id_articulo):
    color = obtener_color_valido(id_articulo)
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


def agregar_color(colores, id_articulo):
    color = obtener_color_valido(id_articulo)
    if color in colores.keys():
        print("\n\t\tYa existe este color.")
    else:
        cantidad = obtener_valor_positivo("Cantidad")
        descuento = obtener_valor_en_rango("Descuento", 0, 100)
        colores[color] = {
            "cantidad": cantidad,
            "descuento": descuento
        }


def modificar_articulos(_pedidos, nro_pedido):
    print("\n\t\tArtículos actuales: ")
    productos = _pedidos[nro_pedido]['productos']
    print(json.dumps(productos, indent=4, ensure_ascii=False))
    codigo = input("Ingrese el código del producto a modificar: ")
    if codigo in productos.keys():
        id_articulo = "1" if codigo == "1334" else "2"
        opcion = ''
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


def modificar_pedido(_pedidos: dict):
    if len(_pedidos) > 0:
        print("\n\t\tPedidos actuales:", end=' ')
        print(", ".join(f"[{key}]" for key in _pedidos.keys()))
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


def eliminar_pedido(_pedidos):
    print(json.dumps(_pedidos, indent=4, ensure_ascii=False))
    nro_pedido = input("\n\t\tIngrese el número de órden a eliminar: ")
    if nro_pedido in _pedidos.keys():
        del _pedidos[nro_pedido]
    else:
        print("\n\tNo existe ningún pedido con ese número.")


def listar_pedidos(_pedidos):
    if len(_pedidos) > 0:
        print(json.dumps(_pedidos, indent=4, ensure_ascii=False))
    else:
        print("\n\t\tNo existen pedidos cargados actualmente.")


def pedidos_abm(_pedidos: dict):
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


def imprimir_total(articulos_enviados, ciudad):
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


def obtener_valor_total_por_ciudad(_pedidos: dict, ciudad: str):
    articulos_enviados: dict = {}
    for k1 in _pedidos.keys():
        if _pedidos[k1]["enviado"] and (_pedidos[k1]["ciudad"].upper() == ciudad.upper()):
            productos = _pedidos[k1]["productos"]
            descuento = _pedidos[k1]["descuento"]
            for k2 in productos.keys():
                colores = productos[k2]
                precio = PRECIO_BOTELLA if k2 == "1334" else PRECIO_VASO
                for k3 in colores.keys():
                    cantidad = colores[k3]["cantidad"]
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


pedidos = cargar_pedidos()
pedidos_abm(pedidos)
