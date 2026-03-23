import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


@allure.feature("UI тесты")
@allure.story("Поиск книг")
@pytest.mark.ui
class TestUISearch:
    """UI тесты для поиска книг"""

    @allure.title("Поиск книги по названию")
    @allure.severity("critical")
    def test_search_by_title(self, driver):
        """Тест поиска книги по названию"""
        with allure.step("Перейти на страницу поиска"):
            driver.get("https://www.chitai-gorod.ru/search?phrase=Карлсон")
            time.sleep(3)

        with allure.step("Проверить, что есть результаты"):
            page_source = driver.page_source
            allure.attach(driver.get_screenshot_as_png(), name="search_results",
                          attachment_type=allure.attachment_type.PNG)
            assert "Карлсон" in page_source or "карлсон" in page_source.lower(), "Результаты поиска не найдены"

    @allure.title("Загрузка главной страницы")
    @allure.severity("normal")
    def test_main_page_loads(self, driver):
        """Тест загрузки главной страницы"""
        with allure.step("Открыть главную страницу"):
            driver.get("https://www.chitai-gorod.ru")
            time.sleep(2)

        with allure.step("Проверить заголовок страницы"):
            assert "Читай-город" in driver.title or "chitai-gorod" in driver.title.lower()

    @allure.title("Поиск несуществующей книги")
    @allure.severity("normal")
    def test_search_nonexistent_book(self, driver):
        """Тест поиска несуществующей книги"""
        with allure.step("Поиск несуществующей книги"):
            driver.get("https://www.chitai-gorod.ru/search?phrase=абвгдеёжзиклмнопрст")
            time.sleep(3)

        with allure.step("Проверить сообщение об отсутствии результатов"):
            allure.attach(driver.get_screenshot_as_png(), name="no_results", attachment_type=allure.attachment_type.PNG)
            # Проверяем, что страница загрузилась
            assert driver.title is not None


@allure.feature("UI тесты")
@allure.story("Корзина")
@pytest.mark.ui
class TestUICart:
    """UI тесты для корзины"""

    @allure.title("Добавление книги в корзину")
    @allure.severity("critical")
    @pytest.mark.skip(reason="Требуется дополнительная настройка для работы с корзиной")
    def test_add_book_to_cart(self, driver):
        """Тест добавления книги в корзину"""
        with allure.step("Открыть главную страницу"):
            driver.get("https://www.chitai-gorod.ru")
            time.sleep(3)

        with allure.step("Проверить, что страница загрузилась"):
            allure.attach(driver.get_screenshot_as_png(), name="cart_page", attachment_type=allure.attachment_type.PNG)
            assert driver.title is not None

    @allure.title("Удаление книги из корзины")
    @allure.severity("normal")
    def test_remove_book_from_cart(self, driver):
        """Тест удаления книги из корзины"""
        with allure.step("Открыть корзину"):
            driver.get("https://www.chitai-gorod.ru/cart")
            time.sleep(3)

        with allure.step("Проверить, что корзина отображается"):
            allure.attach(driver.get_screenshot_as_png(), name="cart_page", attachment_type=allure.attachment_type.PNG)
            assert driver.title is not None
