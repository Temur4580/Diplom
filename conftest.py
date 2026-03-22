import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_autoinstaller
import requests
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


@pytest.fixture(scope="function")
def driver(request):
    """Фикстура для создания WebDriver"""
    # Автоматическая установка ChromeDriver
    chromedriver_autoinstaller.install()

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

        # Используем chromedriver_autoinstaller
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.maximize_window()

        yield driver
        driver.quit()
    else:
        pytest.skip(f"Browser {browser} not supported")


@pytest.fixture(scope="function")
def api_client():
    """Фикстура для API клиента"""

    class SimpleAPIClient:
        def __init__(self):
            self.base_url = "https://www.chitai-gorod.ru"
            self.session = requests.Session()
            self.session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"
            })

        def get(self, endpoint, params=None):
            """GET запрос"""
            url = f"{self.base_url}{endpoint}"
            return self.session.get(url, params=params, timeout=10)

        def post(self, endpoint, json=None, params=None):
            """POST запрос"""
            url = f"{self.base_url}{endpoint}"
            if params:
                return self.session.post(url, params=params, json=json, timeout=10)
            return self.session.post(url, json=json, timeout=10)

    return SimpleAPIClient()



