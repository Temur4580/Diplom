import pytest
import requests
import allure
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def pytest_addoption(parser):
    """Добавление командных опций"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания WebDriver"""
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser.lower() == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Добавляем user-agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
        except:
            # Если не работает через Service, пробуем без него
            driver = webdriver.Chrome(options=options)

        driver.implicitly_wait(10)
        driver.maximize_window()

        # Добавляем задержку для загрузки
        time.sleep(1)

        yield driver
        driver.quit()
    else:
        pytest.skip(f"Browser {browser} not supported")


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента с повторными попытками"""

    class SimpleAPIClient:
        def __init__(self):
            self.base_url = "https://www.chitai-gorod.ru"
            self.session = requests.Session()
            self.session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Upgrade-Insecure-Requests": "1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",
            })

        def _make_request(self, method, endpoint, **kwargs):
            """Внутренний метод для выполнения запросов с повторными попытками"""
            url = f"{self.base_url}{endpoint}"
            max_retries = 3
            retry_delay = 2

            for attempt in range(max_retries):
                try:
                    response = getattr(self.session, method)(url, timeout=10, **kwargs)
                    return response
                except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                    if attempt == max_retries - 1:
                        allure.attach(
                            f"Error after {max_retries} attempts: {str(e)}",
                            name=f"Request Error - {endpoint}",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        # Возвращаем ответ с ошибкой
                        response = requests.Response()
                        response.status_code = 503
                        response._content = b'{"error": "service unavailable"}'
                        return response
                    time.sleep(retry_delay)
            return None

        def get(self, endpoint, params=None, headers=None):
            """GET запрос с повторными попытками"""
            kwargs = {"params": params}
            if headers:
                kwargs["headers"] = headers
            return self._make_request("get", endpoint, **kwargs)

        def post(self, endpoint, json=None, params=None, headers=None):
            """POST запрос с повторными попытками"""
            kwargs = {"json": json}
            if params:
                kwargs["params"] = params
            if headers:
                kwargs["headers"] = headers
            return self._make_request("post", endpoint, **kwargs)

    return SimpleAPIClient()


def pytest_configure(config):
    """Конфигурация pytest"""
    config.addinivalue_line(
        "markers", "ui: mark test as UI test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as API test"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )


@pytest.fixture(scope="session", autouse=True)
def setup_allure_environment():
    """Настройка Allure окружения"""
    allure.attach(
        "Diplom Project - Chitai-Gorod Tests",
        name="Project",
        attachment_type=allure.attachment_type.TEXT
    )
    allure.attach(
        f"Python {__import__('sys').version}",
        name="Python Version",
        attachment_type=allure.attachment_type.TEXT
    )




