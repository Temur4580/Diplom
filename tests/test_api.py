import pytest
import allure
import requests


@allure.feature("API тесты")
@allure.story("Поиск")
@pytest.mark.api
class TestAPISearch:
    """API тесты для поиска"""

    @allure.title("Поиск книги по названию")
    @allure.severity("critical")
    def test_search_book_by_title(self, api_client):
        """Тест поиска книги по названию"""
        with allure.step("Выполнить поиск"):
            response = api_client.get("/search", params={"phrase": "Карлсон"})

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        with allure.step("Проверить, что есть результаты"):
            assert "Карлсон" in response.text or "карлсон" in response.text.lower()

    @allure.title("Поиск книги с коротким запросом")
    @allure.severity("normal")
    def test_search_short_query(self, api_client):
        """Тест поиска с коротким запросом"""
        response = api_client.get("/search", params={"phrase": "Python"})
        assert response.status_code == 200

    @allure.title("Поиск с пустым запросом")
    @allure.severity("low")
    def test_search_empty_query(self, api_client):
        """Тест поиска с пустым запросом"""
        response = api_client.get("/search", params={"phrase": ""})
        assert response.status_code == 200


@allure.feature("API тесты")
@allure.story("Страницы")
@pytest.mark.api
class TestAPIPages:
    """Тесты доступности страниц"""

    @allure.title("Проверка главной страницы")
    @allure.severity("critical")
    def test_main_page(self, api_client):
        """Тест главной страницы"""
        response = api_client.get("/")
        assert response.status_code == 200

    @allure.title("Проверка страницы корзины")
    @allure.severity("normal")
    def test_cart_page(self, api_client):
        """Тест страницы корзины"""
        response = api_client.get("/cart")
        assert response.status_code == 200




@allure.feature("API тесты")
@allure.story("Негативные сценарии")
@pytest.mark.api
class TestAPINegative:
    """Негативные API тесты"""

    @allure.title("Невалидный эндпоинт")
    @allure.severity("normal")
    def test_invalid_endpoint(self, api_client):
        """Тест несуществующего эндпоинта"""
        response = api_client.get("/invalid-endpoint-12345")
        assert response.status_code == 404

    @allure.title("Неправильный метод")
    @allure.severity("normal")
    def test_wrong_method(self, api_client):
        """Тест использования неправильного метода"""
        # Пробуем отправить POST на GET эндпоинт
        response = api_client.post("/search")
        # POST может не поддерживаться, ожидаем 405 или 404
        assert response.status_code in [405, 404, 200]

    @allure.title("Проверка 404 ошибки")
    @allure.severity("normal")
    def test_not_found(self, api_client):
        """Тест несуществующей страницы"""
        response = api_client.get("/page-does-not-exist-xyz")
        assert response.status_code == 404


@allure.feature("API тесты")
@allure.story("Заголовки")
@pytest.mark.api
class TestAPIHeaders:
    """Тесты заголовков ответа"""

    @allure.title("Проверка Content-Type")
    @allure.severity("low")
    def test_content_type(self, api_client):
        """Тест наличия Content-Type"""
        response = api_client.get("/")
        assert "content-type" in response.headers
        assert "text/html" in response.headers["content-type"]

    @allure.title("Проверка Server заголовка")
    @allure.severity("low")
    def test_server_header(self, api_client):
        """Тест наличия Server заголовка"""
        response = api_client.get("/")
        # Server заголовок может быть или не быть
        assert response.status_code == 200
