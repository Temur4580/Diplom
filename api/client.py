import requests
from typing import Optional, Dict, Any
from config.settings import settings
import allure


class APIClient:
    """API клиент для взаимодействия с сервисом"""

    def __init__(self, token: Optional[str] = None):
        self.base_url = settings.API_BASE_URL
        self.session = requests.Session()
        self.token = token
        self._setup_headers()

    def _setup_headers(self) -> None:
        """Настройка заголовков запросов"""
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        self.session.headers.update(headers)

    def set_token(self, token: str) -> None:
        """Установка токена авторизации"""
        self.token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    @allure.step("GET запрос к {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict] = None) -> requests.Response:
        """Выполнение GET запроса"""
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"URL: {url}, params: {params}"):
            response = self.session.get(url, params=params)
            return response

    @allure.step("POST запрос к {endpoint}")
    def post(self, endpoint: str, data: Optional[Dict] = None,
             json: Optional[Dict] = None) -> requests.Response:
        """Выполнение POST запроса"""
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"URL: {url}, data: {data or json}"):
            response = self.session.post(url, data=data, json=json)
            return response

    @allure.step("PUT запрос к {endpoint}")
    def put(self, endpoint: str, data: Optional[Dict] = None) -> requests.Response:
        """Выполнение PUT запроса"""
        url = f"{self.base_url}{endpoint}"
        with allure.step(f"URL: {url}, data: {data}"):
            response = self.session.put(url, json=data)
            return response

    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint: str) -> requests.Response:
        """Выполнение DELETE запроса"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        return response
