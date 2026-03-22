from typing import Optional, Dict, Any
from api.client import APIClient
from config.test_data import test_data
import allure


class APIEndpoints:
    """Класс для работы с API эндпоинтами"""

    def __init__(self, client: APIClient):
        self.client = client

    @allure.step("Поиск книги по названию")
    def search_books(self, phrase: str, page: int = 1,
                     per_page: int = 60) -> Any:
        """Поиск книг по названию"""
        params = {
            "products[page]": page,
            "products[per-page]": per_page,
            "phrase": phrase,
        }
        return self.client.get("/search", params=params)

    @allure.step("Поиск книг по категории")
    def get_category(self, slug: str) -> Any:
        """Получение категории книг"""
        params = {"slug": slug}
        return self.client.get("/categories", params=params)

    @allure.step("Добавление книги в корзину")
    def add_to_cart(self, product_id: int) -> Any:
        """Добавление товара в корзину"""
        data = {"id": product_id}
        return self.client.post("/cart", json=data)

    @allure.step("Поиск с неправильным методом")
    def search_with_wrong_method(self, phrase: str) -> Any:
        """Выполнение поиска с неправильным HTTP методом"""
        params = {
            "customerCityId": test_data.CUSTOMER_CITY_ID,
            "phrase": phrase,
            "abTestGroup": test_data.AB_TEST_GROUP
        }
        return self.client.put(test_data.ENDPOINTS["facet_search"], data=params)

    @allure.step("Запрос на невалидный эндпоинт")
    def invalid_endpoint(self) -> Any:
        """Запрос на несуществующий эндпоинт"""
        return self.client.get("/web/api/v1")

    @allure.step("Добавление в корзину с невалидным ID")
    def add_to_cart_invalid_id(self, product_id: str) -> Any:
        """Добавление товара с невалидным ID"""
        data = {"id": product_id}
        return self.client.post(test_data.ENDPOINTS["cart"], json=data)

    @allure.step("Запрос категории без slug")
    def get_category_without_slug(self) -> Any:
        """Запрос категории без обязательного параметра"""
        params = {"slug": ""}
        return self.client.get(test_data.ENDPOINTS["categories"], params=params)
