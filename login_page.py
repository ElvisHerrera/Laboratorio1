from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("https://www.saucedemo.com/")

    def login(self, usuario, clave):
        self.wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(usuario)
        self.driver.find_element(By.ID, "password").send_keys(clave)
        self.wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    def get_error_message(self):
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        ).text