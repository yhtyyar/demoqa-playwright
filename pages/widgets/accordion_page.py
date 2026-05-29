"""Страница Accordian — раскрывающиеся панели."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class AccordionPage(BasePage):
    """Page Object для страницы https://demoqa.com/accordian.

    Ключевое открытие: DemoQA НЕ использует Bootstrap .card классы.
    Единственные стабильные точки входа — heading IDs:
      #section1Heading, #section2Heading, #section3Heading
    Состояние открытости проверяем через nextElementSibling + getBoundingClientRect.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AccordionPage":
        """Открыть страницу Accordian."""
        super().open("/accordian")
        return self

    def click_section(self, section_number: int) -> "AccordionPage":
        """Кликнуть по триггеру секции через heading ID.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        self.page.evaluate(
            """(n) => {
                const heading = document.getElementById('section' + n + 'Heading');
                if (!heading) return;
                const trigger =
                    heading.querySelector('[data-toggle="collapse"]') ||
                    heading.querySelector('[data-bs-toggle="collapse"]') ||
                    heading.querySelector('button') ||
                    heading;
                trigger.click();
            }""",
            section_number,
        )
        self.page.wait_for_timeout(600)
        return self

    def is_section_open(self, section_number: int) -> bool:
        """Проверить открытость секции через nextElementSibling heading'а.

        Находим #sectionNHeading (гарантированно есть в DOM),
        берём следующий sibling-элемент (контент секции),
        проверяем высоту через getBoundingClientRect.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если контент секции имеет высоту > 0.
        """
        return bool(
            self.page.evaluate(
                """(n) => {
                    const heading = document.getElementById('section' + n + 'Heading');
                    if (!heading) return false;
                    const content = heading.nextElementSibling;
                    if (!content) return false;
                    return content.getBoundingClientRect().height > 0;
                }""",
                section_number,
            )
        )

    def ensure_section_open(self, section_number: int) -> "AccordionPage":
        """Гарантировать открытость секции. Кликнуть если закрыта.

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
            innerText содержимого секции.
        """
        try:
            text = self.page.evaluate(
                """(n) => {
                    const heading = document.getElementById('section' + n + 'Heading');
                    if (!heading) return '';
                    const content = heading.nextElementSibling;
                    return content ? (content.innerText || '') : '';
                }""",
                section_number,
            )
            return str(text).strip() if text else ""
        except Exception:
            return ""

    def heading_exists(self, section_number: int) -> bool:
        """Проверить наличие heading'а секции в DOM.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если #sectionNHeading найден.
        """
        return self.page.locator(f"#section{section_number}Heading").count() > 0
