import pytest
import allure
from config.test_data import test_data
from utils.helpers import Helpers


@allure.feature("API тесты")
@allure.story("Поиск")
@pytest.mark.api
class TestAPISearch:
    """API тесты для поиска"""

    @allure.title("Поиск книги по названию")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_search_book_by_title(self, api_client):
        """Тест поиска книги по названию"""
        response = api_client.search_books(test_data.SEARCH_QUERY)
        Helpers.attach_response(response, "Search Response")

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверить, что в ответе есть данные"):
            data = response.json()
            assert "data" in data, "В ответе отсутствует поле 'data'"

    @allure.title("Поиск книги по категории")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_by_category(self, api_client):
        """Тест поиска книг по категории"""
        response = api_client.get_category(test_data.CATEGORY_SLUG)
        Helpers.attach_response(response, "Category Response")

        with allure.step("Проверить статус код"):
            assert response.status_code == 200

        with allure.step("Проверить содержимое ответа"):
            response_text = response.text
            assert "psihologiya" in response_text.lower(), \
                "В ответе нет ожидаемого содержимого"


@allure.feature("API тесты")
@allure.story("Корзина")
@pytest.mark.api
class TestAPICart:
    """API тесты для корзины"""

    @allure.title("Добавление книги в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_to_cart(self, api_client):
        """Тест добавления книги в корзину"""
        response = api_client.add_to_cart(test_data.PRODUCT_ID)
        Helpers.attach_response(response, "Add to Cart Response")

        with allure.step("Проверить статус код"):
            assert response.status_code == 200

        with allure.step("Проверить время ответа"):
            assert response.elapsed.total_seconds() < 1, \
                f"Время ответа превышает 1 секунду: {response.elapsed.total_seconds()}"

    @allure.title("Добавление в корзину без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_to_cart_unauthorized(self, api_client_unauthorized):
        """Тест добавления в корзину без авторизации"""
        response = api_client_unauthorized.add_to_cart(test_data.PRODUCT_ID)
        Helpers.attach_response(response, "Unauthorized Response")

        with allure.step("Проверить статус код 401"):
            assert response.status_code == 401, \
                f"Ожидался статус 401, получен {response.status_code}"

    @allure.title("Добавление в корзину с невалидным ID")
    @allure.severity(allure.severity_level.NORMAL)
    def test_add_to_cart_invalid_id(self, api_client):
        """Тест добавления товара с невалидным ID"""
        response = api_client.add_to_cart_invalid_id(test_data.INVALID_PRODUCT_ID)
        Helpers.attach_response(response, "Invalid ID Response")

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}"


@allure.feature("API тесты")
@allure.story("Негативные сценарии")
@pytest.mark.api
class TestAPINegative:
    """Негативные API тесты"""

    @allure.title("Поиск с неправильным HTTP методом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_wrong_method(self, api_client):
        """Тест использования неправильного HTTP метода"""
        response = api_client.search_with_wrong_method(test_data.SEARCH_QUERY_SHORT)
        Helpers.attach_response(response, "Wrong Method Response")

        with allure.step("Проверить статус код 405"):
            assert response.status_code == 405, \
                f"Ожидался статус 405, получен {response.status_code}"

    @allure.title("Запрос на невалидный эндпоинт")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_endpoint(self, api_client):
        """Тест запроса на несуществующий эндпоинт"""
        response = api_client.invalid_endpoint()
        Helpers.attach_response(response, "Invalid Endpoint Response")

        with allure.step("Проверить статус код 404"):
            assert response.status_code == 404, \
                f"Ожидался статус 404, получен {response.status_code}"

    @allure.title("Запрос категории без slug параметра")
    @allure.severity(allure.severity_level.NORMAL)
    def test_category_without_slug(self, api_client):
        """Тест запроса категории без обязательного параметра"""
        response = api_client.get_category_without_slug()
        Helpers.attach_response(response, "No Slug Response")

        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}"


@allure.feature("API тесты")
@allure.story("Дополнительные проверки")
@pytest.mark.api
class TestAPIAdditional:
    """Дополнительные API тесты"""

    @allure.title("Поиск книги с коротким запросом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_short_query(self, api_client):
        """Тест поиска с коротким запросом"""
        response = api_client.search_books(test_data.SEARCH_QUERY_SHORT)

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что найдены результаты"):
            data = response.json()
            assert len(data.get("data", [])) > 0, "Не найдено результатов"

    @allure.title("Поиск книги с пустым запросом")
    @allure.severity(allure.severity_level.LOW)
    def test_search_empty_query(self, api_client):
        """Тест поиска с пустым запросом"""
        response = api_client.search_books("")

        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что возвращаются популярные книги"):
            data = response.json()
            assert "data" in data, "В ответе отсутствует поле 'data'"
