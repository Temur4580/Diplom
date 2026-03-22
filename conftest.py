import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.settings import settings
from api.client import APIClient
from api.endpoints import APIEndpoints
import allure


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


@pytest.fixture(scope="session")
def browser_name(request):
    """Фикстура для получения имени браузера"""
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def headless_mode(request):
    """Фикстура для получения режима headless"""
    return request.config.getoption("--headless") or settings.HEADLESS


@pytest.fixture(scope="function")
def driver(browser_name, headless_mode):
    """Фикстура для создания и закрытия WebDriver"""
    driver = None

    if browser_name.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if headless_mode:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
    elif browser_name.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        if headless_mode:
            options.add_argument("--headless")
        driver = webdriver.Firefox(
            service=Service(GeckoDriverManager().install()),
            options=options
        )
    else:
        raise ValueError(f"Browser {browser_name} is not supported")

    driver.implicitly_wait(settings.IMPLICIT_WAIT)
    driver.maximize_window()

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента"""
    # Используем токен из настроек
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3VzZXItcmlnaHQiLCJzdWIiOjIzNTMwNTUzLCJpYXQiOjE3NjU3MzcxOTMsImV4cCI6MTc2NTc0MDc5MywidHlwZSI6MjAsImp0aSI6IjAxOWIxZTIzLTVmNDMtN2RmOS1hYWQ1LTUwOGEyZGMwNGYzOSIsInJvbGVzIjoxMH0.FtUCFn0LUBiHRQzlw5iheZ6xaSLhsgHQq4e-9gnDDFg"
    client = APIClient(token=token)
    return APIEndpoints(client)


@pytest.fixture(scope="function")
def api_client_unauthorized():
    """Фикстура для API клиента без авторизации"""
    client = APIClient()
    return APIEndpoints(client)


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
