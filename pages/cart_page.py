from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class CartPage(BasePage):
    """Страница корзины"""

    # Locators
    CART_ITEMS = (By.CSS_SELECTOR, "[data-testid='cart-item']")
    CART_ITEM_TITLE = (By.CSS_SELECTOR, "[data-testid='cart-item-title']")
    CART_ITEM_PRICE = (By.CSS_SELECTOR, "[data-testid='cart-item-price']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-testid='checkout-button']")
    EMPTY_CART_MESSAGE = (By.CSS_SELECTOR, "[data-testid='empty-cart']")
    REMOVE_ITEM_BUTTON = (By.CSS_SELECTOR, "[data-testid='remove-item']")

    @allure.step("Получить количество товаров в корзине")
    def get_cart_items_count(self) -> int:
        """Получить количество товаров в корзине"""
        return len(self.find_elements(self.CART_ITEMS))

    @allure.step("Получить название первого товара в корзине")
    def get_first_item_title(self) -> str:
        """Получить название первого товара в корзине"""
        titles = self.find_elements(self.CART_ITEM_TITLE)
        if titles:
            return titles[0].text
        return ""

    @allure.step("Удалить первый товар из корзины")
    def remove_first_item(self) -> None:
        """Удалить первый товар из корзины"""
        remove_buttons = self.find_elements(self.REMOVE_ITEM_BUTTON)
        if remove_buttons:
            remove_buttons[0].click()

    @allure.step("Проверить, что корзина пуста")
    def is_cart_empty(self) -> bool:
        """Проверить, пуста ли корзина"""
        return self.is_element_visible(self.EMPTY_CART_MESSAGE, timeout=5)
