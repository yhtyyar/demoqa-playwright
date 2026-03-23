"""Глобальные фикстуры pytest."""

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.settings import Settings
from pages.main_page import MainPage
from utils.logger import logger


@pytest.fixture(scope="session")
def browser():
    """Создать экземпляр браузера на всю тестовую сессию.

    Поддерживаемые движки (BROWSER):
        - chromium — Blink (Google Chrome, Яндекс Браузер, Edge)
        - firefox  — Gecko (Mozilla Firefox)
        - webkit   — WebKit (Safari)

    Дополнительно (BROWSER_CHANNEL):
        - chrome, msedge — запуск реального браузера вместо встроенного
    """
    with sync_playwright() as p:
        browser_args = {
            "headless": Settings.HEADLESS,
            "slow_mo": 100 if not Settings.HEADLESS else 0,
        }

        if Settings.BROWSER_CHANNEL:
            browser_args["channel"] = Settings.BROWSER_CHANNEL

        if Settings.BROWSER == "firefox":
            browser_type = p.firefox
        elif Settings.BROWSER == "webkit":
            browser_type = p.webkit
        else:
            browser_type = p.chromium

        logger.info(
            "Запуск браузера: engine=%s, channel=%s, headless=%s",
            Settings.BROWSER,
            Settings.BROWSER_CHANNEL or "default",
            Settings.HEADLESS,
        )

        browser = browser_type.launch(**browser_args)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser):
    """Создать контекст браузера для каждого теста."""
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        ignore_https_errors=True,
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Создать новую страницу для каждого теста."""
    page = context.new_page()
    page.set_default_timeout(Settings.TIMEOUT)
    yield page
    page.close()


@pytest.fixture(scope="function")
def main_page(page: Page) -> MainPage:
    """Создать объект главной страницы и открыть её."""
    return MainPage(page).open()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Сделать скриншот при падении теста."""
    outcome = yield
    report = outcome.get_result()

    if Settings.SCREENSHOT_ON_FAIL and report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            screenshot_path = str(Settings.SCREENSHOTS_DIR / f"{item.name}.png")
            try:
                page.screenshot(path=screenshot_path)
            except Exception:
                pass
