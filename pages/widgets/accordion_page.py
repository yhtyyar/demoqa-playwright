"""Страница Accordian — раскрывающиеся панели."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class AccordionPage(BasePage):
    """Page Object для страницы https://demoqa.com/accordian."""

    SECTION1_TITLE = "#section1Heading"
    SECTION2_TITLE = "#section2Heading"
    SECTION3_TITLE = "#section3Heading"
    SECTION1_CONTENT = "#section1Content"
    SECTION2_CONTENT = "#section2Content"
    SECTION3_CONTENT = "#section3Content"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AccordionPage":
        """Открыть страницу Accordian."""
        super().open("/accordian")
        return self

    @property
    def section1_title(self) -> Locator:
        """Заголовок первой секции."""
        return self.page.locator(self.SECTION1_TITLE)

    @property
    def section2_title(self) -> Locator:
        """Заголовок второй секции."""
        return self.page.locator(self.SECTION2_TITLE)

    @property
    def section3_title(self) -> Locator:
        """Заголовок третьей секции."""
        return self.page.locator(self.SECTION3_TITLE)

    @property
    def section1_content(self) -> Locator:
        """Контент первой секции."""
        return self.page.locator(self.SECTION1_CONTENT)

    @property
    def section2_content(self) -> Locator:
        """Контент второй секции."""
        return self.page.locator(self.SECTION2_CONTENT)

    @property
    def section3_content(self) -> Locator:
        """Контент третьей секции."""
        return self.page.locator(self.SECTION3_CONTENT)

    def click_section(self, section_number: int) -> "AccordionPage":
        """Кликнуть по заголовку секции для раскрытия/сворачивания.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        titles = {
            1: self.section1_title,
            2: self.section2_title,
            3: self.section3_title,
        }
        self.click(titles[section_number])
        self.page.wait_for_timeout(400)
        return self

    def is_section_open(self, section_number: int) -> bool:
        """Проверить, открыта ли секция.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если секция раскрыта.
        """
        contents = {
            1: self.section1_content,
            2: self.section2_content,
            3: self.section3_content,
        }
        return self.is_visible(contents[section_number])

    def get_section_text(self, section_number: int) -> str:
        """Получить текст содержимого секции.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Текст открытой секции.
        """
        contents = {
            1: self.section1_content,
            2: self.section2_content,
            3: self.section3_content,
        }
        return self.get_text(contents[section_number])
