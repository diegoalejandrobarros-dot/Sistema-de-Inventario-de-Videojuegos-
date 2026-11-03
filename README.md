# Sistema de Inventario de Videojuegos

Aplicación de consola en Python que administra el inventario de una tienda de videojuegos. Permite registrar, consultar, actualizar y eliminar productos (CRUD) y registrar ventas, guardando todo en una base de datos **SQLite** y aplicando el **patrón DAO**.

## Propósito

Practicar la separación de responsabilidades en capas (modelo, acceso a datos, lógica de negocio e interfaz) y el uso de SQLite desde Python. Los datos **se conservan entre ejecuciones** en el archivo `tienda.db`, que se crea automáticamente la primera vez.

## Estructura del proyecto

| Archivo | Responsabilidad |
|---|---|
| `modelo.py` | Clase `Producto` (id, nombre, precio, stock). |
| `base_datos.py` | `obtener_conexion()` abre la conexión con SQLite e `inicializar_bd()` crea la tabla `productos`. |
| `producto_dao.py` | Clase `ProductoDAO`: **único** lugar con consultas SQL (`crear`, `listar`, `buscar_por_id`, `actualizar`, `actualizar_stock`, `eliminar`). |
| `producto_servicio.py` | Clase `ProductoServicio`: validaciones y reglas de negocio (`registrar`, `listar`, `buscar`, `actualizar`, `eliminar`, `vender`). |
| `main.py` | Menú interactivo. Usa solo los métodos del servicio; no contiene SQL. |
| `pruebas.py` | Pruebas automáticas (`unittest`) que usan una base de datos temporal. |

Flujo de dependencias: `main.py` → `ProductoServicio` → `ProductoDAO` → `base_datos` (SQLite).

## Funcionalidades

1. **Registrar videojuego**: solicita nombre, precio y cantidad disponible.
2. **Mostrar inventario**: lista ID, nombre, precio y stock de todos los videojuegos.
3. **Buscar videojuego**: consulta por ID e informa si no existe.
4. **Actualizar videojuego**: modifica nombre, precio y stock de un producto existente.
5. **Eliminar videojuego**: elimina por ID (pide confirmación `s/n`).
6. **Vender unidades**: pide el ID y la cantidad, y descuenta del inventario.
7. **Salir**: finaliza la aplicación.

### Validaciones implementadas

- El nombre no puede estar vacío (ni contener solo espacios).
- El precio debe ser mayor que cero (también se rechazan `nan` e `inf`).
- El stock no puede ser negativo (0 sí es válido).
- La cantidad a vender debe ser mayor que cero.
- No se puede vender más de lo disponible; en ese caso el stock se conserva.
- Se informa cuando el ID no existe (buscar, actualizar, eliminar y vender).
- Las entradas no numéricas se vuelven a pedir en lugar de cerrar el programa; cualquier error inesperado se captura en el menú, y `Ctrl+C` / `Ctrl+D` cierran de forma ordenada.

## Cómo ejecutarlo

Requisitos: **Python 3.8 o superior**. No necesita instalar librerías externas (`sqlite3` viene con Python).

```bash
git clone <URL-DE-TU-REPOSITORIO>
cd <carpeta-del-repositorio>
python main.py        # en Linux/macOS: python3 main.py
```

Para correr las pruebas automáticas:

```bash
python -m unittest pruebas -v
```

> El videojuego de ejemplo que antes se registraba automáticamente fue eliminado de `main.py`, por lo que ya no se generan duplicados en cada ejecución.
> Si ya habías ejecutado el proyecto base, es posible que tengas un `tienda.db` con ese producto de ejemplo; bórralo para empezar con el inventario vacío.

## Evidencias de las pruebas

Los siguientes fragmentos son salida real de la aplicación (el menú se muestra de forma compacta). Todas las ejecuciones usan el mismo archivo `tienda.db`, por eso el estado se arrastra de una prueba a la siguiente.

### 1. Registrar Resident Evil 4 (precio 180000, stock 10) — operación exitosa

```text
--- MENU (1-7) ---
Seleccione una opcion: 1

--- Registrar videojuego ---
Nombre: Resident Evil 4
Precio: 180000
Cantidad disponible: 10
[OK] Producto guardado correctamente (ID 1).

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 2. Registrar un segundo videojuego y mostrar el inventario

```text
--- MENU (1-7) ---
Seleccione una opcion: 1

--- Registrar videojuego ---
Nombre: Hades
Precio: 70000
Cantidad disponible: 4
[OK] Producto guardado correctamente (ID 2).

--- MENU (1-7) ---
Seleccione una opcion: 2

--- Inventario ---
ID   Nombre                                        Precio   Stock
-----------------------------------------------------------------
1    Resident Evil 4                          $180,000.00      10
2    Hades                                     $70,000.00       4

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 3. Buscar un ID existente y uno inexistente (operación rechazada)

```text
--- MENU (1-7) ---
Seleccione una opcion: 3

--- Buscar videojuego ---
ID del videojuego: 1
  ID:     1
  Nombre: Resident Evil 4
  Precio: $180,000.00
  Stock:  10

--- MENU (1-7) ---
Seleccione una opcion: 3

--- Buscar videojuego ---
ID del videojuego: 99
[ERROR] No existe un videojuego con ID 99

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 4. Actualizar un producto

```text
--- MENU (1-7) ---
Seleccione una opcion: 4

--- Actualizar videojuego ---
ID del videojuego: 2
Datos actuales:
  ID:     2
  Nombre: Hades
  Precio: $70,000.00
  Stock:  4
Ingrese los nuevos datos:
Nuevo nombre: Hades II
Nuevo precio: 95000
Nuevo stock: 8
[OK] Videojuego actualizado:
  ID:     2
  Nombre: Hades II
  Precio: $95,000.00
  Stock:  8

--- MENU (1-7) ---
Seleccione una opcion: 2

--- Inventario ---
ID   Nombre                                        Precio   Stock
-----------------------------------------------------------------
1    Resident Evil 4                          $180,000.00      10
2    Hades II                                  $95,000.00       8

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 5. Vender 3 unidades (stock 10 → 7) y vender 20 unidades (operación rechazada)

```text
--- MENU (1-7) ---
Seleccione una opcion: 6

--- Vender unidades ---
ID del videojuego: 1
Resident Evil 4 - Stock disponible: 10
Cantidad a vender: 3
[OK] Venta realizada: 3 x Resident Evil 4 = $540,000.00
     Stock: 10 -> 7

--- MENU (1-7) ---
Seleccione una opcion: 6

--- Vender unidades ---
ID del videojuego: 1
Resident Evil 4 - Stock disponible: 7
Cantidad a vender: 20
[ERROR] Stock insuficiente: se pidieron 20 unidades y solo hay 7 disponibles

--- MENU (1-7) ---
Seleccione una opcion: 2

--- Inventario ---
ID   Nombre                                        Precio   Stock
-----------------------------------------------------------------
1    Resident Evil 4                          $180,000.00       7
2    Hades II                                  $95,000.00       8

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 6. Eliminar un producto

```text
--- MENU (1-7) ---
Seleccione una opcion: 5

--- Eliminar videojuego ---
ID del videojuego: 2
Eliminar 'Hades II'? (s/n): s
[OK] 'Hades II' fue eliminado del inventario.

--- MENU (1-7) ---
Seleccione una opcion: 2

--- Inventario ---
ID   Nombre                                        Precio   Stock
-----------------------------------------------------------------
1    Resident Evil 4                          $180,000.00       7

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 7. Persistencia: nueva ejecución del programa, mismos datos

```text
--- MENU (1-7) ---
Seleccione una opcion: 2

--- Inventario ---
ID   Nombre                                        Precio   Stock
-----------------------------------------------------------------
1    Resident Evil 4                          $180,000.00       7

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### 8. Validaciones: entradas incorrectas rechazadas sin cerrar el programa

Nombre vacío, precio negativo, precio no numérico, stock negativo, cantidad no numérica, ventas de 0, de un valor negativo y de más unidades que el stock, actualización con stock negativo y opciones de menú inválidas. Al final, el inventario no cambió.

```text
--- MENU (1-7) ---
Seleccione una opcion: 1

--- Registrar videojuego ---
Nombre: 
Precio: 100
Cantidad disponible: 5
[ERROR] El nombre no puede estar vacio

--- MENU (1-7) ---
Seleccione una opcion: 1

--- Registrar videojuego ---
Nombre: Juego X
Precio: -5
Cantidad disponible: 5
[ERROR] El precio debe ser mayor que cero

--- MENU (1-7) ---
Seleccione una opcion: 1

--- Registrar videojuego ---
Nombre: Juego X
Precio: abc
[ERROR] Ingrese un numero valido (ej: 180000 o 59.99).
Precio: 100
Cantidad disponible: -1
[ERROR] El stock no puede ser negativo

--- MENU (1-7) ---
Seleccione una opcion: 1

--- Registrar videojuego ---
Nombre: Juego X
Precio: 100
Cantidad disponible: diez
[ERROR] Ingrese un numero entero valido (ej: 10).
Cantidad disponible: -3
[ERROR] El stock no puede ser negativo

--- MENU (1-7) ---
Seleccione una opcion: 6

--- Vender unidades ---
ID del videojuego: 1
Resident Evil 4 - Stock disponible: 7
Cantidad a vender: 0
[ERROR] La cantidad a vender debe ser mayor que cero

--- MENU (1-7) ---
Seleccione una opcion: 6

--- Vender unidades ---
ID del videojuego: 1
Resident Evil 4 - Stock disponible: 7
Cantidad a vender: -2
[ERROR] La cantidad a vender debe ser mayor que cero

--- MENU (1-7) ---
Seleccione una opcion: 6

--- Vender unidades ---
ID del videojuego: 1
Resident Evil 4 - Stock disponible: 7
Cantidad a vender: dos
[ERROR] Ingrese un numero entero valido (ej: 10).
Cantidad a vender: 100
[ERROR] Stock insuficiente: se pidieron 100 unidades y solo hay 7 disponibles

--- MENU (1-7) ---
Seleccione una opcion: 4

--- Actualizar videojuego ---
ID del videojuego: 1
Datos actuales:
  ID:     1
  Nombre: Resident Evil 4
  Precio: $180,000.00
  Stock:  7
Ingrese los nuevos datos:
Nuevo nombre: Resident Evil 4
Nuevo precio: 180000
Nuevo stock: -3
[ERROR] El stock no puede ser negativo

--- MENU (1-7) ---
Seleccione una opcion: 9
[ERROR] Opcion no valida. Elija un numero del 1 al 7.

--- MENU (1-7) ---
Seleccione una opcion: hola
[ERROR] Opcion no valida. Elija un numero del 1 al 7.

--- MENU (1-7) ---
Seleccione una opcion: 2

--- Inventario ---
ID   Nombre                                        Precio   Stock
-----------------------------------------------------------------
1    Resident Evil 4                          $180,000.00       7

--- MENU (1-7) ---
Seleccione una opcion: 7
Hasta pronto.
```

### Pruebas automáticas

`python -m unittest pruebas -v` → **20 pruebas, todas exitosas** (cubren los 8 casos de la tabla del taller, cada validación obligatoria y la persistencia entre ejecuciones).

### Capturas de pantalla
#REGISTRO EXITOSO
<img width="409" height="285" alt="Captura" src="https://github.com/user-attachments/assets/181686ee-57ef-4742-abb4-3f83ff126043" />


<!-- Agrega aquí tus capturas, por ejemplo:
![Registro exitoso](evidencias/01_registro.png)
![Venta rechazada](evidencias/02_venta_rechazada.png)
-->
