"""Pruebas automaticas del taller.

Cada prueba usa una base de datos temporal, asi que NO toca tu tienda.db.
Ejecutar con:  python -m unittest pruebas -v
"""

import os
import shutil
import tempfile
import unittest
from unittest import mock

import base_datos
from base_datos import inicializar_bd
from producto_dao import ProductoDAO
from producto_servicio import ProductoServicio


class PruebasInventario(unittest.TestCase):
    def setUp(self):
        # Redirige la conexion a un archivo temporal para esta prueba
        self.carpeta = tempfile.mkdtemp()
        ruta = os.path.join(self.carpeta, "prueba.db")
        parche = mock.patch.object(base_datos, "RUTA_BD", ruta)
        parche.start()
        self.addCleanup(parche.stop)
        self.addCleanup(shutil.rmtree, self.carpeta, True)

        inicializar_bd()
        self.servicio = ProductoServicio(ProductoDAO())

    # ---- Casos de la tabla del taller -------------------------------
    def test_registrar_resident_evil_4(self):
        p = self.servicio.registrar("Resident Evil 4", 180000, 10)
        self.assertEqual(p.id, 1)
        guardado = self.servicio.buscar(p.id)
        self.assertEqual(guardado.nombre, "Resident Evil 4")
        self.assertEqual(guardado.precio, 180000)
        self.assertEqual(guardado.stock, 10)

    def test_mostrar_inventario(self):
        self.servicio.registrar("Resident Evil 4", 180000, 10)
        self.servicio.registrar("Hades", 70000, 4)
        nombres = [p.nombre for p in self.servicio.listar()]
        self.assertEqual(nombres, ["Resident Evil 4", "Hades"])

    def test_inventario_vacio(self):
        self.assertEqual(self.servicio.listar(), [])

    def test_buscar_id_existente(self):
        p = self.servicio.registrar("Hades", 70000, 4)
        self.assertEqual(self.servicio.buscar(p.id).nombre, "Hades")

    def test_actualizar_producto_queda_guardado(self):
        p = self.servicio.registrar("Hades", 70000, 4)
        self.servicio.actualizar(p.id, "Hades II", 95000, 8)
        # Se consulta de nuevo a SQLite para confirmar que quedo guardado
        guardado = self.servicio.buscar(p.id)
        self.assertEqual(
            (guardado.nombre, guardado.precio, guardado.stock),
            ("Hades II", 95000, 8),
        )

    def test_vender_3_unidades_stock_10_a_7(self):
        p = self.servicio.registrar("Resident Evil 4", 180000, 10)
        self.servicio.vender(p.id, 3)
        self.assertEqual(self.servicio.buscar(p.id).stock, 7)

    def test_vender_20_se_rechaza_y_conserva_stock(self):
        p = self.servicio.registrar("Resident Evil 4", 180000, 10)
        with self.assertRaisesRegex(ValueError, "Stock insuficiente"):
            self.servicio.vender(p.id, 20)
        self.assertEqual(self.servicio.buscar(p.id).stock, 10)

    def test_buscar_id_inexistente(self):
        with self.assertRaisesRegex(ValueError, "No existe"):
            self.servicio.buscar(999)

    def test_eliminar_producto(self):
        p = self.servicio.registrar("Hades", 70000, 4)
        self.servicio.eliminar(p.id)
        self.assertEqual(self.servicio.listar(), [])
        with self.assertRaisesRegex(ValueError, "No existe"):
            self.servicio.buscar(p.id)

    # ---- Validaciones obligatorias ----------------------------------
    def test_nombre_vacio(self):
        for nombre in ("", "   "):
            with self.assertRaisesRegex(ValueError, "nombre"):
                self.servicio.registrar(nombre, 100, 1)

    def test_precio_invalido(self):
        for precio in (0, -5, float("nan"), float("inf")):
            with self.assertRaisesRegex(ValueError, "precio"):
                self.servicio.registrar("Juego", precio, 1)

    def test_stock_negativo(self):
        with self.assertRaisesRegex(ValueError, "stock"):
            self.servicio.registrar("Juego", 100, -1)

    def test_stock_cero_es_valido(self):
        p = self.servicio.registrar("Juego agotado", 100, 0)
        self.assertEqual(self.servicio.buscar(p.id).stock, 0)

    def test_registro_invalido_no_guarda_nada(self):
        with self.assertRaises(ValueError):
            self.servicio.registrar("", 100, 1)
        self.assertEqual(self.servicio.listar(), [])

    def test_venta_cantidad_cero_o_negativa(self):
        p = self.servicio.registrar("Juego", 100, 5)
        for cantidad in (0, -2):
            with self.assertRaisesRegex(ValueError, "mayor que cero"):
                self.servicio.vender(p.id, cantidad)
        self.assertEqual(self.servicio.buscar(p.id).stock, 5)

    def test_vender_todo_el_stock_es_valido(self):
        p = self.servicio.registrar("Juego", 100, 5)
        self.servicio.vender(p.id, 5)
        self.assertEqual(self.servicio.buscar(p.id).stock, 0)

    def test_vender_id_inexistente(self):
        with self.assertRaisesRegex(ValueError, "No existe"):
            self.servicio.vender(999, 1)

    def test_actualizar_y_eliminar_id_inexistente(self):
        with self.assertRaisesRegex(ValueError, "No existe"):
            self.servicio.actualizar(999, "X", 10, 1)
        with self.assertRaisesRegex(ValueError, "No existe"):
            self.servicio.eliminar(999)

    def test_actualizar_con_datos_invalidos_no_modifica(self):
        p = self.servicio.registrar("Hades", 70000, 4)
        with self.assertRaises(ValueError):
            self.servicio.actualizar(p.id, "Nuevo", -1, 4)
        guardado = self.servicio.buscar(p.id)
        self.assertEqual((guardado.nombre, guardado.precio), ("Hades", 70000))

    # ---- Persistencia entre ejecuciones -----------------------------
    def test_datos_se_conservan_entre_ejecuciones(self):
        self.servicio.registrar("Hades", 70000, 4)
        # "Segunda ejecucion": objetos nuevos sobre el mismo archivo .db
        inicializar_bd()  # no debe borrar ni duplicar nada
        otro_servicio = ProductoServicio(ProductoDAO())
        self.assertEqual([p.nombre for p in otro_servicio.listar()], ["Hades"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
