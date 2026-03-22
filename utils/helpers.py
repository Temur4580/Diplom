import allure
from typing import Any
import json


class Helpers:
    """Вспомогательные функции"""

    @staticmethod
    @allure.step("Сохранение скриншота")
    def take_screenshot(driver, name: str = "screenshot") -> None:
        """Сделать скриншот и прикрепить к allure"""
        screenshot = driver.get_screenshot_as_png()
        allure.attach(
            screenshot,
            name=f"{name}.png",
            attachment_type=allure.attachment_type.PNG
        )

    @staticmethod
    @allure.step("Сохранение лога ответа API")
    def attach_response(response: Any, name: str = "API Response") -> None:
        """Прикрепить ответ API к allure отчету"""
        try:
            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name=name,
                attachment_type=allure.attachment_type.JSON
            )
        except:
            allure.attach(
                str(response.text),
                name=name,
                attachment_type=allure.attachment_type.TEXT
            )

    @staticmethod
    @allure.step("Генерация уникального email")
    def generate_unique_email() -> str:
        """Генерация уникального email для тестов"""
        import time
        return f"test_user_{int(time.time())}@example.com"
