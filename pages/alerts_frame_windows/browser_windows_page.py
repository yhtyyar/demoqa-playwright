"""Страница Browser Windows — новые вкладки и окна."""

from playwright.sync_api import BrowserContext, Locator, Page

from pages.base_page import BasePage


class BrowserWindowsPage(BasePage):
    """Page Object для страницы https://demoqa.com/browser-windows.

    Демонстрирует перехват новых вкладок/окон через Playwright context.expect_page()
    — возможность, недоступная в Selenium без сложных workarounds.
    """

    BUTTON_NEW_TAB = "#tabButton"
    BUTTON_NEW_WINDOW = "#windowButton"
    BUTTON_NEW_WINDOW_MSG = "#messageWindowButton"
    HEADING_TEXT = "#sampleHeading"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.context: BrowserContext = page.context

    def open(self) -> "BrowserWindowsPage":
        """Открыть страницу Browser Windows."""
        super().open("/browser-windows")
        return self

    @property
    def new_tab_button(self) -> Locator:
        """Кнопка открытия новой вкладки."""
        return self.page.locator(self.BUTTON_NEW_TAB)

    @property
    def new_window_button(self) -> Locator:
        """Кнопка открытия нового окна."""
        return self.page.locator(self.BUTTON_NEW_WINDOW)

    def open_new_tab_and_get_text(self) -> str:
        """Открыть новую вкладку и получить текст заголовка.

        Используем context.expect_page() — Playwright-специфичный способ
        перехватить новую страницу до завершения её загрузки.

        Returns:
            Текст заголовка #sampleHeading на новой вкладке.
        """
        with self.context.expect_page() as new_page_info:
            self.click(self.new_tab_button)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        heading = new_page.locator(self.HEADING_TEXT)
        heading.wait_for(state="visible", timeout=10000)
        text = heading.text_content() or ""
        new_page.close()
        return text

    def open_new_window_and_get_text(self) -> str:
        """Открыть новое окно и получить текст заголовка.

        Returns:
            Текст заголовка #sampleHeading в новом окне.
        """
        with self.context.expect_page() as new_page_info:
            self.click(self.new_window_button)
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        heading = new_page.locator(self.HEADING_TEXT)
        heading.wait_for(state="visible", timeout=10000)
        text = heading.text_content() or ""
        new_page.close()
        return text
