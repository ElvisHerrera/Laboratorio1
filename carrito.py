from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    # Login
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    # Esperar inventario
    wait.until(EC.visibility_of_element_located((By.ID, "inventory_container")))
    print("Login exitoso")

    # Agregar producto al carrito
    wait.until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    ).click()
    print("Producto agregado al carrito")

    # Validar que el carrito muestre 1
    carrito = wait.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    if carrito.text == "1":
        print("Prueba exitosa: el carrito muestra 1 producto")
    else:
        print("Prueba fallida: el carrito no muestra 1")

finally:
    driver.quit()