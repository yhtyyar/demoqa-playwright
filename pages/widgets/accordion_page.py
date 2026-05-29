"""Страница Accordian — раскрывающиеся панели."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class AccordionPage(BasePage):
    """Page Object для страницы https://demoqa.com/accordian.

    DemoQA использует Bootstrap 4 collapse. Контент-дивы (#section1Content и т.д.)
    могут отсутствовать в DOM или иметь другую структуру в зависимости от версии.
    Надёжный подход — проверять aria-expanded на кнопке: Bootstrap всегда его выставляет.
    """

    # Кнопки внутри заголовков (именно они активируют collapse)
    SECTION1_BTN = "#section1Heading button"
    SECTION2_BTN = "#section2Heading button"
    SECTION3_BTN = "#section3Heading button"

    # Текст берём из .card-body внутри карточки по порядку
    SECTION1_BODY = ".card:nth-child(1) .card-body"
    SECTION2_BODY = ".card:nth-child(2) .card-body"
    SECTION3_BODY = ".card:nth-child(3) .card-body"

    _BTN_MAP = {1: "SECTION1_BTN", 2: "SECTION2_BTN", 3: "SECTION3_BTN"}
    _BODY_MAP = {1: "SECTION1_BODY", 2: "SECTION2_BODY", 3: "SECTION3_BODY"}

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AccordionPage":
        """Открыть страницу Accordian."""
        super().open("/accordian")
        return self

    def click_section(self, section_number: int) -> "AccordionPage":
        """Кликнуть по кнопке секции для раскрытия/сворачивания.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        selector = getattr(self, self._BTN_MAP[section_number])
        self.click(self.page.locator(selector))
        self.page.wait_for_timeout(500)
        return self

    def is_section_open(self, section_number: int) -> bool:
        """Проверить, открыта ли секция через aria-expanded на кнопке.

        Bootstrap 4 устанавливает aria-expanded='true' на button когда секция открыта.
        Это надёжнее проверки CSS-класса collapse-div (тот может не иметь фиксированного ID).

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если aria-expanded='true' на кнопке секции.
        """
        selector = getattr(self, self._BTN_MAP[section_number])
        locator = self.page.locator(selector)
        if locator.count() == 0:
            return False
        aria = locator.get_attribute("aria-expanded", timeout=5000) or "false"
        return aria.lower() == "true"

    def get_section_text(self, section_number: int) -> str:
        """Получить текст содержимого секции.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Текст карточки-тела открытой секции.
        """
        selector = getattr(self, self._BODY_MAP[section_number])
        try:
            return self.page.locator(selector).text_content(timeout=5000) or ""
        except Exception:
            return ""
