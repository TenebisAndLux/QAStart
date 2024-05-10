import selenium
from selenium import webdriver
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

LITECART_LOGIN_URL = "http://admin:admin@localhost:81/litecart/admin/login.php"
LITECART_LOGOUT_URL = "http://localhost:81/litecart/admin/logout.php"


def value_or_none(func):
    try:
        return func()
    except:
        return None


def open_litecart(driver: WebDriver):
    driver.get(LITECART_LOGIN_URL)


def login_user(wait: WebDriverWait, username, password):
    username_field = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    login_button = wait.until(EC.element_to_be_clickable((By.NAME, "login")))

    username_field.clear()
    username_field.send_keys(username)
    password_field.clear()
    password_field.send_keys(password)
    login_button.click()

    print(f"User with username: {username} and password: {password} logged in")


def open_translations_page(wait: WebDriverWait):
    translations_link = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[child::span[text() = 'Translations']]")
        )
    )
    translations_link.click()


options = webdriver.FirefoxOptions()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
wait = WebDriverWait(driver, 1)

open_litecart(driver)
login_user(wait, "admin", "admin")
open_translations_page(wait)

count = 0
while True:
    elements = driver.find_elements(
        By.XPATH, "//input[@type = 'checkbox' and contains(@name, 'translations')]"
    )
    for element in elements:
        element.click()
        count += 1

    next_button = value_or_none(
        lambda: driver.find_element(
            By.XPATH, "//a[@class = 'page button' and text() = 'Next']"
        )
    )
    if next_button is None or not next_button.is_enabled():
        break

    next_button.click()

print(f"Count: {count}")

driver.get(LITECART_LOGOUT_URL)

driver.quit()
