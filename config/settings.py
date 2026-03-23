"""Глобальные настройки проекта."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Настройки тестового окружения."""

    BASE_URL: str = os.getenv("BASE_URL", "https://demoqa.com")
    BROWSER: str = os.getenv("BROWSER", "chromium")
    BROWSER_CHANNEL: str = os.getenv("BROWSER_CHANNEL", "")
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    TIMEOUT: int = int(os.getenv("TIMEOUT", "30000"))
    SCREENSHOT_ON_FAIL: bool = os.getenv("SCREENSHOT_ON_FAIL", "true").lower() == "true"

    # Пути
    ROOT_DIR: Path = Path(__file__).parent.parent
    REPORTS_DIR: Path = ROOT_DIR / "reports"
    SCREENSHOTS_DIR: Path = REPORTS_DIR / "screenshots"

    # Таймауты (увеличены для Firefox/WebKit в CI)
    PAGE_LOAD_TIMEOUT: int = 60000
    EXPECT_TIMEOUT: int = 15000
    ACTION_TIMEOUT: int = 10000

    # Данные для тестов
    TEST_USER: dict = {
        "full_name": "John Doe",
        "email": "john.doe@example.com",
        "current_address": "123 Main Street, New York",
        "permanent_address": "456 Oak Avenue, Los Angeles",
    }

    @classmethod
    def create_directories(cls) -> None:
        """Создать необходимые директории для отчётов и скриншотов."""
        cls.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        cls.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        (cls.REPORTS_DIR / "html").mkdir(parents=True, exist_ok=True)
        (cls.REPORTS_DIR / "xml").mkdir(parents=True, exist_ok=True)


Settings.create_directories()
