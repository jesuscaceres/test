# Logistik
Contiene un archivo principal para probar el reconocimiento de imágenes utilizando opencv.

Para que todo funcione, modifiquen la ruta de sus archivos .jpg para que la función los pueda leer.

# Pedidos
Contiene un archivo principal para la lectura de pedidos desde un archivo .csv y la posibiliad de crear, modificar y eliminar pedidos

**¿Qué se puede modificar?**
1. Fecha
2. Cliente
3. Ciudad
4. Provincia
5. Productos (color, cantidad y descuento)

Estoy utilizando como primera idea una estructura de pedidos en este formato parecido a JSON.
Según las opiniones de todos, vemos si la dejamos así o cambiamos. De esta forma me resultó mas cómodo trabajar por ahora.

```json
{
    "1": {
        "fecha": "01/11/2021",
        "cliente": "Juan Alvarez",
        "ciudad": "Villa María",
        "provincia": "Córdoba",
        "productos": {
            "1334": {
                "azul": {
                    "cantidad": 36
                },
                "amarillo": {
                    "cantidad": 12
                }
            },
            "568": {
                "azul": {
                    "cantidad": 12
                },
                "negro": {
                    "cantidad": 6
                }
            }
        },
        "descuento": 5.0,
        "enviado": false
    },
    "2": {
        "fecha": "01/11/2021",
        "cliente": "Carlos Rodriguez",
        "ciudad": "Parana",
        "provincia": "Santa Fe",
        "productos": {
            "1334": {
                "rojo": {
                    "cantidad": 5
                },
                "negro": {
                    "cantidad": 5
                }
            }
        },
        "descuento": 0.0,
        "enviado": false
    }
}
```
