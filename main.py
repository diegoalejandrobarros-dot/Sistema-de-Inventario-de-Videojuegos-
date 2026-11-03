# mostrar el menu y recibir datos
from base_datos import inicializar_bd
from producto_dao import ProductoDAO
from producto_servicio import ProductoServicio


# ---------------------------------------------------------------------
# Lectura segura de datos: una entrada incorrecta no cierra el programa
# ---------------------------------------------------------------------
def leer_texto(mensaje):
    return input(mensaje).strip()


def leer_entero(mensaje):
    while True:
        valor = input(mensaje).strip()
        try:
            return int(valor)
        except ValueError:
            print("[ERROR] Ingrese un numero entero valido (ej: 10).")


def leer_decimal(mensaje):
    while True:
        valor = input(mensaje).strip()
        try:
            return float(valor)
        except ValueError:
            print("[ERROR] Ingrese un numero valido (ej: 180000 o 59.99).")


# ---------------------------------------------------------------------
# Presentacion
# ---------------------------------------------------------------------
def mostrar_menu():
    print("\n===== INVENTARIO DE VIDEOJUEGOS =====")
    print("1. Registrar videojuego")
    print("2. Mostrar inventario")
    print("3. Buscar videojuego")
    print("4. Actualizar videojuego")
    print("5. Eliminar videojuego")
    print("6. Vender unidades")
    print("7. Salir")


def mostrar_detalle(producto):
    print(f"  ID:     {producto.id}")
    print(f"  Nombre: {producto.nombre}")
    print(f"  Precio: ${producto.precio:,.2f}")
    print(f"  Stock:  {producto.stock}")


def mostrar_tabla(productos):
    print(f"{'ID':<5}{'Nombre':<36}{'Precio':>16}{'Stock':>8}")
    print("-" * 65)
    for p in productos:
        precio = f"${p.precio:,.2f}"
        print(f"{p.id:<5}{p.nombre:<36.35}{precio:>16}{p.stock:>8}")


# ---------------------------------------------------------------------
# Opciones del menu (solo usan los metodos del servicio)
# ---------------------------------------------------------------------
def registrar_videojuego(servicio):
    print("\n--- Registrar videojuego ---")
    nombre = leer_texto("Nombre: ")
    precio = leer_decimal("Precio: ")
    stock = leer_entero("Cantidad disponible: ")
    producto = servicio.registrar(nombre, precio, stock)
    print(f"[OK] Producto guardado correctamente (ID {producto.id}).")


def mostrar_inventario(servicio):
    print("\n--- Inventario ---")
    productos = servicio.listar()
    if not productos:
        print("El inventario esta vacio.")
        return
    mostrar_tabla(productos)


def buscar_videojuego(servicio):
    print("\n--- Buscar videojuego ---")
    id_producto = leer_entero("ID del videojuego: ")
    producto = servicio.buscar(id_producto)
    mostrar_detalle(producto)


def actualizar_videojuego(servicio):
    print("\n--- Actualizar videojuego ---")
    id_producto = leer_entero("ID del videojuego: ")
    actual = servicio.buscar(id_producto)
    print("Datos actuales:")
    mostrar_detalle(actual)
    print("Ingrese los nuevos datos:")
    nombre = leer_texto("Nuevo nombre: ")
    precio = leer_decimal("Nuevo precio: ")
    stock = leer_entero("Nuevo stock: ")
    producto = servicio.actualizar(id_producto, nombre, precio, stock)
    print("[OK] Videojuego actualizado:")
    mostrar_detalle(producto)


def eliminar_videojuego(servicio):
    print("\n--- Eliminar videojuego ---")
    id_producto = leer_entero("ID del videojuego: ")
    producto = servicio.buscar(id_producto)
    confirmacion = leer_texto(f"Eliminar '{producto.nombre}'? (s/n): ").lower()
    if confirmacion not in ("s", "si"):
        print("Operacion cancelada.")
        return
    servicio.eliminar(id_producto)
    print(f"[OK] '{producto.nombre}' fue eliminado del inventario.")


def vender_unidades(servicio):
    print("\n--- Vender unidades ---")
    id_producto = leer_entero("ID del videojuego: ")
    producto = servicio.buscar(id_producto)
    print(f"{producto.nombre} - Stock disponible: {producto.stock}")
    cantidad = leer_entero("Cantidad a vender: ")
    stock_anterior = producto.stock
    producto = servicio.vender(id_producto, cantidad)
    total = cantidad * producto.precio
    print(f"[OK] Venta realizada: {cantidad} x {producto.nombre} = ${total:,.2f}")
    print(f"     Stock: {stock_anterior} -> {producto.stock}")


# ---------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------
def main():
    # Preparar la base de datos (crea la tabla solo si no existe)
    inicializar_bd()

    # Crear el servicio, que usa el DAO para hablar con la base de datos
    servicio = ProductoServicio(ProductoDAO())

    acciones = {
        "1": registrar_videojuego,
        "2": mostrar_inventario,
        "3": buscar_videojuego,
        "4": actualizar_videojuego,
        "5": eliminar_videojuego,
        "6": vender_unidades,
    }

    try:
        while True:
            mostrar_menu()
            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "7":
                print("Hasta pronto.")
                break

            accion = acciones.get(opcion)
            if accion is None:
                print("[ERROR] Opcion no valida. Elija un numero del 1 al 7.")
                continue

            try:
                accion(servicio)
            except ValueError as error:  # reglas de negocio incumplidas
                print(f"[ERROR] {error}")
            except EOFError:
                raise  # fin de la entrada: lo maneja el bloque de afuera
            except Exception as error:  # red de seguridad: no cerrar el programa
                print(f"[ERROR] Ocurrio un problema inesperado: {error}")
    except (KeyboardInterrupt, EOFError):
        print("\nAplicacion finalizada.")


if __name__ == "__main__":
    main()
