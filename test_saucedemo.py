import unittest
from selenium import webdriver
from login_page import LoginPage
from inventory_page import InventoryPage
from reporte_html import GeneradorHTMLTestRunner

class TestSauceDemo(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_login_exitoso(self):
        login = LoginPage(self.driver)
        inventory = InventoryPage(self.driver)

        login.open()
        login.login("standard_user", "secret_sauce")
        inventory.wait_inventory_loaded()

        self.assertIn("inventory", self.driver.current_url)

    def test_login_fallido(self):
        login = LoginPage(self.driver)

        login.open()
        login.login("usuario_incorrecto", "clave_incorrecta")

        self.assertIn("Epic sadface", login.get_error_message())

    def test_agregar_producto_al_carrito(self):
        login = LoginPage(self.driver)
        inventory = InventoryPage(self.driver)

        login.open()
        login.login("standard_user", "secret_sauce")
        inventory.wait_inventory_loaded()
        inventory.add_backpack_to_cart()

        self.assertEqual(inventory.get_cart_count(), "1")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    runner = GeneradorHTMLTestRunner(archivo_html="reporte_pruebas.html", verbosity=2)
    unittest.main(testRunner=runner, exit=False)