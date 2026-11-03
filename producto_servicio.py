#aplicar las reglas del negocio
import math

from modelo import Producto


class ProductoServicio:

    def __init__(self, dao):
        self.dao = dao

    # validaciones comunes (se usan al registrar y al actualizar)
    def _validar_datos(self, nombre, precio, stock):

        if nombre.strip() == "":
            raise ValueError("El nombre no puede estar vacio")

        # math.isfinite descarta 'nan' e 'inf', que float() si acepta
        if not math.isfinite(precio):
            raise ValueError("El precio debe ser un numero valido")

        if precio <= 0:
            raise ValueError("El precio debe ser mayor que cero")

        if stock < 0:
            raise ValueError("El stock no puede ser negativo")

        return nombre.strip()

    # 1. REGISTRAR PRODUCTO
    def registrar(self, nombre, precio, stock):

        nombre = self._validar_datos(nombre, precio, stock)

        producto = Producto(None, nombre, precio, stock)

        return self.dao.crear(producto)

    # 2. LISTAR INVENTARIO
    def listar(self):
        return self.dao.listar()

    # 3. BUSCAR PRODUCTO POR ID
    def buscar(self, id_producto):

        producto = self.dao.buscar_por_id(id_producto)

        if producto is None:
            raise ValueError(f"No existe un videojuego con ID {id_producto}")

        return producto

    # 4. ACTUALIZAR PRODUCTO
    def actualizar(self, id_producto, nombre, precio, stock):

        nombre = self._validar_datos(nombre, precio, stock)

        producto = self.buscar(id_producto)  # lanza error si no existe

        producto.nombre = nombre
        producto.precio = precio
        producto.stock = stock

        self.dao.actualizar(producto)

        return producto

    # 5. ELIMINAR PRODUCTO
    def eliminar(self, id_producto):

        self.buscar(id_producto)  # lanza error si no existe

        self.dao.eliminar(id_producto)

    # 6. VENDER UNIDADES
    def vender(self, id_producto, cantidad):

        if cantidad <= 0:
            raise ValueError("La cantidad a vender debe ser mayor que cero")

        producto = self.buscar(id_producto)

        if cantidad > producto.stock:
            raise ValueError(
                f"Stock insuficiente: se pidieron {cantidad} unidades "
                f"y solo hay {producto.stock} disponibles"
            )

        producto.stock = producto.stock - cantidad

        self.dao.actualizar_stock(producto.id, producto.stock)

        return producto
