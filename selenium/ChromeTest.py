from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

# Запускаем браузер Chrome
driver = webdriver.Chrome()

# Открываем веб-страницу
driver.get("https://www.google.com")

# Находим поле ввода для поиска
search_box = driver.find_element(by=By.NAME, value="q")

# Вводим поисковый запрос
search_box.send_keys("Selenium")

# Отправляем форму поиска (нажимаем Enter)
search_box.send_keys(Keys.ENTER)

# Находим первый результат поиска
first_result = driver.find_element(by=By.XPATH, value="//a[@href]")

# Закрываем браузер
driver.quit()
