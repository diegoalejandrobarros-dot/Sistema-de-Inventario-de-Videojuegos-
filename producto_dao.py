#ejecutar las operaciones sql
from base_datos import obtener_conexion
from modelo import Producto

class ProductoDAO:
    
    #1. crear un producto
    def crear(self, producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        
        sql = """ 
            INSERT INTO productos (nombre, precio, stock)
            VALUES (?, ?, ?)
        """
        
        cursor.execute(sql,(producto.nombre, producto.precio, producto.stock))
        producto.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        
        return producto

    #2. listar todos los productos
    def listar(self):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT id, nombre, precio, stock FROM productos ORDER BY id"

        cursor.execute(sql)
        filas = cursor.fetchall()
        conexion.close()

        productos = []
        for fila in filas:
            productos.append(Producto(fila[0], fila[1], fila[2], fila[3]))

        return productos

    #3. buscar un producto por id (devuelve None si no existe)
    def buscar_por_id(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "SELECT id, nombre, precio, stock FROM productos WHERE id = ?"

        cursor.execute(sql, (id_producto,))
        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None

        return Producto(fila[0], fila[1], fila[2], fila[3])

    #4. actualizar nombre, precio y stock de un producto
    def actualizar(self, producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = """
            UPDATE productos
            SET nombre = ?, precio = ?, stock = ?
            WHERE id = ?
        """

        cursor.execute(sql, (producto.nombre, producto.precio, producto.stock, producto.id))
        modificadas = cursor.rowcount
        conexion.commit()
        conexion.close()

        return modificadas > 0

    #5. actualizar solo el stock (se usa en las ventas)
    def actualizar_stock(self, id_producto, nuevo_stock):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "UPDATE productos SET stock = ? WHERE id = ?"

        cursor.execute(sql, (nuevo_stock, id_producto))
        modificadas = cursor.rowcount
        conexion.commit()
        conexion.close()

        return modificadas > 0

    #6. eliminar un producto por id
    def eliminar(self, id_producto):
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        sql = "DELETE FROM productos WHERE id = ?"

        cursor.execute(sql, (id_producto,))
        eliminadas = cursor.rowcount
        conexion.commit()
        conexion.close()

        return eliminadas > 0
