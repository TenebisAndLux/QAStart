import unittest
import selenium
from selenium import webdriver
import selenium.common
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

LITECART_LOGIN_URL = "http://admin:admin@localhost:81/litecart/admin/login.php"
LITECART_BASE_LOGIN_URL = "http://localhost:81/litecart/admin/login.php"
LITECART_LOGOUT_URL = "http://localhost:81/litecart/admin/logout.php"


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


def open_users_page(wait: WebDriverWait):
    users_link = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[child::span[text() = 'Users']]"))
    )
    users_link.click()


def register_user(driver: WebDriver, wait: WebDriverWait, username, password):
    register_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[@class = 'button' and contains(text(), 'Create New User')]")
        )
    )
    register_button.click()

    username_field = wait.until(EC.visibility_of_element_located((By.NAME, "username")))
    password_field = wait.until(EC.visibility_of_element_located((By.NAME, "password")))
    confirm_password_field = wait.until(
        EC.visibility_of_element_located((By.NAME, "confirmed_password"))
    )
    save_button = wait.until(EC.element_to_be_clickable((By.NAME, "save")))

    username_field.send_keys(username)
    password_field.send_keys(password)
    confirm_password_field.send_keys(password)
    save_button.click()

    assert user_exists(driver, username)

    print(f"User with username: {username} and password: {password} registered")


def open_user_edit(wait: WebDriverWait, username):
    edit_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//a[text() = '{username}' and ancestor::tr[contains(@class, 'row')]/td/a]",
            )
        )
    )
    edit_button.click()


def set_user_status(wait: WebDriverWait, username: str, status: bool):
    user_selector = wait.until(
        EC.element_to_be_clickable(
            (
                By.XPATH,
                f"//input[ancestor::tr[contains(@class, 'row')]/td/a[text() = '{username}']]",
            )
        )
    )
    user_selector.click()

    status_button = wait.until(
        EC.element_to_be_clickable(
            (
                By.NAME,
                "enable" if status else "disable",
            )
        )
    )
    status_button.click()

    verify_user_status(wait, username, status)


def verify_user_status(wait: WebDriverWait, username: str, status: bool):
    open_user_edit(wait, username)

    status_checkbox = wait.until(EC.element_to_be_clickable((By.NAME, "status")))
    cancel_button = wait.until(EC.element_to_be_clickable((By.NAME, "cancel")))

    assert status_checkbox.is_selected() == status

    cancel_button.click()


def delete_user(driver: WebDriver, wait: WebDriverWait, username):
    open_user_edit(wait, username)

    delete_button = wait.until(EC.element_to_be_clickable((By.NAME, "delete")))
    delete_button.click()

    alert = wait.until(
        EC.alert_is_present(), "Timed out waiting for delete confirmation"
    )
    alert.accept()

    assert not user_exists(driver, username)

    print(f"User with username: {username} deleted")


def user_exists(driver, username):
    try:
        user_element = driver.find_element(
            By.XPATH,
            f"//a[text() = '{username}' and ancestor::tr[contains(@class, 'row')]/td/a]",
        )
        return user_element is not None
    except selenium.common.exceptions.NoSuchElementException:
        return False


def logout_user(driver: WebDriver):
    driver.get(LITECART_LOGOUT_URL)

    assert driver.current_url == LITECART_BASE_LOGIN_URL

    print("User logged out")


def perform_test(driver: WebDriver, wait: WebDriverWait):
    open_litecart(driver)

    login_user(wait, "admin", "admin")
    open_users_page(wait)

    register_user(driver, wait, "test_user", "test_user_password")
    set_user_status(wait, "test_user", True)
    # verify_user_status(wait, "test_user", True)

    logout_user(driver)

    login_user(wait, "test_user", "test_user_password")
    logout_user(driver)

    login_user(wait, "admin", "admin")
    open_users_page(wait)
    set_user_status(wait, "test_user", False)
    # verify_user_status(wait, "test_user", False)
    delete_user(driver, wait, "test_user")
    logout_user(driver)


class FirefoxTest(unittest.TestCase):
    def setUp(self) -> None:
        options = webdriver.FirefoxOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.addCleanup(self.driver.quit)

    def test_litecart(self):
        perform_test(self.driver, self.wait)


class ChromeTest(unittest.TestCase):
    def setUp(self) -> None:
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

        self.addCleanup(self.driver.quit)

    def test_litecart(self):
        perform_test(self.driver, self.wait)


if __name__ == "__main__":
    import nose2

    nose2.main()
