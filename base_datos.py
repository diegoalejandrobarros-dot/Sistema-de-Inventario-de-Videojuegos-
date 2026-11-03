# gestionar la conexion y crear la tabla
import os
import sqlite3

# La base de datos se guarda junto a este archivo. Asi los datos se conservan
# entre ejecuciones sin importar desde que carpeta se ejecute el programa.
RUTA_BD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tienda.db")

def obtener_conexion():
    conexion = sqlite3.connect(RUTA_BD)
    return conexion

def inicializar_bd():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio INTEGER NOT NULL,
            stock INTEGER NOT NULL
        )
    """)
    
    conexion.commit()
    conexion.close()
