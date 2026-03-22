import os
from pathlib import Path


class Settings:
    # Base URLs
    BASE_URL = "https://www.chitai-gorod.ru"
    API_BASE_URL = "https://web-agr.chitai-gorod.ru"

    # Timeouts
    IMPLICIT_WAIT = 10
    EXPLICIT_WAIT = 20
    PAGE_LOAD_TIMEOUT = 30

    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chrome")

    # Paths
    ROOT_DIR = Path(__file__).parent.parent
    SCREENSHOTS_DIR = ROOT_DIR / "screenshots"

    # Create directories if not exist
    SCREENSHOTS_DIR.mkdir(exist_ok=True)


settings = Settings()
