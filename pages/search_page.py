from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class SearchPage(BasePage):
    """Страница результатов поиска"""

    # Locators
    SEARCH_RESULTS = (By.CSS_SELECTOR, "[data-testid='product-card']")
    PRODUCT_TITLE = (By.CSS_SELECTOR, "[data-testid='product-title']")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "[data-testid='product-price']")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "[data-testid='add-to-cart']")
    NO_RESULTS_MESSAGE = (By.CSS_SELECTOR, "[data-testid='no-results']")

    @allure.step("Получить количество найденных товаров")
    def get_products_count(self) -> int:
        """Получить количество найденных товаров"""
        return len(self.find_elements(self.SEARCH_RESULTS))

    @allure.step("Добавить первый товар в корзину")
    def add_first_product_to_cart(self) -> None:
        """Добавить первый товар в корзину"""
        add_buttons = self.find_elements(self.ADD_TO_CART_BUTTON)
        if add_buttons:
            add_buttons[0].click()

    @allure.step("Получить название первого товара")
    def get_first_product_title(self) -> str:
        """Получить название первого товара"""
        titles = self.find_elements(self.PRODUCT_TITLE)
        if titles:
            return titles[0].text
        return ""
