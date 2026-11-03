# representar los productos como objetos
class Producto:
    """Represemta un producto de la tienda"""
    
    def __init__(self, id, nombre, precio, stock):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.stock = stock