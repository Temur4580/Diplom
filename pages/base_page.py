from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException
from config.settings import settings
import allure


class BasePage:
    """Базовый класс для всех Page Objects"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.EXPLICIT_WAIT)
        self.implicit_wait = settings.IMPLICIT_WAIT

    @allure.step("Открыть страницу {url}")
    def open(self, url: str) -> None:
        """Открыть указанный URL"""
        self.driver.get(url)

    @allure.step("Найти элемент: {locator}")
    def find_element(self, locator: tuple) -> WebElement:
        """Найти элемент с ожиданием"""
        return self.wait.until(
            EC.presence_of_element_located(locator)
        )

    @allure.step("Найти все элементы: {locator}")
    def find_elements(self, locator: tuple) -> list:
        """Найти все элементы"""
        return self.driver.find_elements(*locator)

    @allure.step("Кликнуть на элемент: {locator}")
    def click(self, locator: tuple) -> None:
        """Кликнуть на элемент"""
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    @allure.step("Ввести текст '{text}' в поле: {locator}")
    def input_text(self, locator: tuple, text: str) -> None:
        """Ввести текст в поле"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Получить текст элемента: {locator}")
    def get_text(self, locator: tuple) -> str:
        """Получить текст элемента"""
        return self.find_element(locator).text

    @allure.step("Проверить видимость элемента: {locator}")
    def is_element_visible(self, locator: tuple, timeout: int = 10) -> bool:
        """Проверить видимость элемента"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Скролл до элемента: {locator}")
    def scroll_to_element(self, locator: tuple) -> None:
        """Прокрутить до элемента"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
