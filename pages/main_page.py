from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.settings import settings
import allure


class MainPage(BasePage):
    """Главная страница интернет-магазина"""

    # Locators
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Поиск']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    CART_ICON = (By.CSS_SELECTOR, "[data-testid='cart-icon']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-testid='login-button']")
    CATEGORY_MENU = (By.CSS_SELECTOR, ".categories-menu")

    @allure.step("Открыть главную страницу")
    def open_main_page(self) -> None:
        """Открыть главную страницу"""
        self.open(settings.BASE_URL)

    @allure.step("Выполнить поиск по запросу: {query}")
    def search(self, query: str) -> None:
        """Выполнить поиск книги"""
        self.input_text(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)

    @allure.step("Перейти в корзину")
    def go_to_cart(self) -> None:
        """Перейти в корзину"""
        self.click(self.CART_ICON)

    @allure.step("Открыть категорию: {category_name}")
    def open_category(self, category_name: str) -> None:
        """Открыть категорию книг"""
        category_link = (By.LINK_TEXT, category_name)
        self.click(category_link)
