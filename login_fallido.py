from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()

    wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys("incorrect_user")
    driver.find_element(By.ID, "password").send_keys("incorrect_password")
    driver.find_element(By.ID, "login-button").click()

    error = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )

    if "Epic sadface" in error.text:
        print("Prueba exitosa: error detectado")
        print("Mensaje:", error.text)
    else:
        print("Prueba fallida")

finally:
    driver.quit()