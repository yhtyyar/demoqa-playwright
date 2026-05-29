"""Страница Links — проверка ссылок и API-статусов."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class LinksPage(BasePage):
    """Page Object для страницы https://demoqa.com/links.

    Две группы ссылок:
    1. Навигационные — открывают https://demoqa.com в новой вкладке.
    2. API-ссылки — делают fetch-запрос и показывают HTTP-статус в #linkResponse.
    """

    LINK_HOME_SIMPLE = "#simpleLink"
    LINK_HOME_DYNAMIC = "#dynamicLink"

    LINK_CREATED = "#created"
    LINK_NO_CONTENT = "#no-content"
    LINK_MOVED = "#moved"
    LINK_BAD_REQUEST = "#bad-request"
    LINK_UNAUTHORIZED = "#unauthorized"
    LINK_FORBIDDEN = "#forbidden"
    LINK_NOT_FOUND = "#invalid-url"

    RESPONSE_TEXT = "#linkResponse"

    EXPECTED_STATUS = {
        "created": 201,
        "no-content": 204,
        "moved": 301,
        "bad-request": 400,
        "unauthorized": 401,
        "forbidden": 403,
        "invalid-url": 404,
    }

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "LinksPage":
        """Открыть страницу Links."""
        super().open("/links")
        return self

    @property
    def response_text(self) -> Locator:
        """Блок с ответом от API-ссылки."""
        return self.page.locator(self.RESPONSE_TEXT)

    def click_api_link(self, link_id: str) -> "LinksPage":
        """Кликнуть по API-ссылке и дождаться ответа.

        Args:
            link_id: Значение атрибута id ссылки (например, 'created').

        Returns:
            Экземпляр LinksPage для chaining.
        """
        self.click(self.page.locator(f"#{link_id}"))
        self.wait_for_element(self.response_text)
        self.page.wait_for_timeout(500)
        return self

    def get_response_text(self) -> str:
        """Получить текст последнего API-ответа.

        Returns:
            Текст из #linkResponse.
        """
        return self.get_text(self.response_text)

    def get_response_status(self) -> int:
        """Извлечь числовой HTTP-статус из текста ответа.

        DemoQA возвращает текст вида 'Link has responded with staus 201 and status text Created'.

        Returns:
            Числовой HTTP-статус или 0 если распарсить не удалось.
        """
        text = self.get_response_text()
        for part in text.split():
            if part.isdigit():
                return int(part)
        return 0

    def open_simple_link_in_new_tab(self) -> str:
        """Кликнуть по простой ссылке и получить URL новой вкладки.

        Returns:
            URL открытой вкладки.
        """
        with self.page.context.expect_page() as new_page_info:
            self.click(self.page.locator(self.LINK_HOME_SIMPLE))
        new_page = new_page_info.value
        new_page.wait_for_load_state("domcontentloaded")
        url = new_page.url
        new_page.close()
        return url
