"""Страница Accordian — раскрывающиеся панели."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class AccordionPage(BasePage):
    """Page Object для страницы https://demoqa.com/accordian.

    DemoQA использует Bootstrap 4 collapse. Способы определения открытой секции
    по убыванию надёжности:
      1. .collapse.show count() — МГНОВЕННО, не ждёт DOM-элементы  ← используем
      2. aria-expanded на кнопке — зависит от Bootstrap JS (может быть не выставлен)
      3. is_visible() — ждёт до timeout, неправильно для overflow:hidden
    """

    # Заголовки — для клика используем card-header целиком (надёжнее, чем конкретная кнопка)
    SECTION1_HEADER = ".card:nth-child(1) .card-header"
    SECTION2_HEADER = ".card:nth-child(2) .card-header"
    SECTION3_HEADER = ".card:nth-child(3) .card-header"

    # Открытая секция = .collapse.show внутри карточки (Bootstrap-стандарт)
    SECTION1_OPEN = ".card:nth-child(1) .collapse.show"
    SECTION2_OPEN = ".card:nth-child(2) .collapse.show"
    SECTION3_OPEN = ".card:nth-child(3) .collapse.show"

    # Текст из card-body (доступен всегда, даже когда collapse скрыт через display:none)
    SECTION1_BODY = ".card:nth-child(1) .card-body"
    SECTION2_BODY = ".card:nth-child(2) .card-body"
    SECTION3_BODY = ".card:nth-child(3) .card-body"

    _HEADER_MAP = {1: "SECTION1_HEADER", 2: "SECTION2_HEADER", 3: "SECTION3_HEADER"}
    _OPEN_MAP = {1: "SECTION1_OPEN", 2: "SECTION2_OPEN", 3: "SECTION3_OPEN"}
    _BODY_MAP = {1: "SECTION1_BODY", 2: "SECTION2_BODY", 3: "SECTION3_BODY"}

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AccordionPage":
        """Открыть страницу Accordian."""
        super().open("/accordian")
        return self

    def click_section(self, section_number: int) -> "AccordionPage":
        """Кликнуть по заголовку секции для раскрытия/сворачивания.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        selector = getattr(self, self._HEADER_MAP[section_number])
        self.click(self.page.locator(selector))
        self.page.wait_for_timeout(500)
        return self

    def is_section_open(self, section_number: int) -> bool:
        """Проверить, открыта ли секция через count() на .collapse.show.

        Bootstrap добавляет класс 'show' к открытому .collapse.
        count() возвращает результат мгновенно — не ждёт появления элемента.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если .collapse.show присутствует внутри карточки секции.
        """
        selector = getattr(self, self._OPEN_MAP[section_number])
        return self.page.locator(selector).count() > 0

    def ensure_section_open(self, section_number: int) -> "AccordionPage":
        """Гарантировать, что секция открыта. Кликнуть если закрыта.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        if not self.is_section_open(section_number):
            self.click_section(section_number)
        return self

    def get_section_text(self, section_number: int) -> str:
        """Получить текст содержимого секции.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Текст card-body секции.
        """
        selector = getattr(self, self._BODY_MAP[section_number])
        try:
            return self.page.locator(selector).text_content(timeout=5000) or ""
        except Exception:
            return ""
