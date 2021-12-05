from main import *


def crear_txt(nombre_archivo: str, stock: dict):
    with open(f"Archivos/{nombre_archivo}.txt", "w+") as archivo:
        for key, value in stock.items():
            archivo.write(f"{key} {str(value)}\n")


def crear_archivos_txt():
    botellas, vasos = get_stock()
    if len(botellas) > 0:
        print("\n\tCreando botellas.txt ...")
        crear_txt("botellas", botellas)
        print("\n\tArchivo botellas.txt creado!")

    if len(vasos) > 0:
        print("\n\tCreando vasos.txt ...")
        crear_txt("vasos", vasos)
        print("\n\tArchivo vasos.txt creado!")


crear_archivos_txt()
