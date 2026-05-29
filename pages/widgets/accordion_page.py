"""Страница Accordian — раскрывающиеся панели."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class AccordionPage(BasePage):
    """Page Object для страницы https://demoqa.com/accordian.

    DemoQA accordion — внешний сайт, разметка может меняться.
    Вместо CSS-классов или aria-атрибутов используем getBoundingClientRect():
    высота card-body > 0 = секция открыта, высота == 0 = закрыта.
    Это работает для любой реализации (Bootstrap 4/5, кастомный JS).
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AccordionPage":
        """Открыть страницу Accordian."""
        super().open("/accordian")
        return self

    def is_section_open(self, section_number: int) -> bool:
        """Проверить открытость секции через высоту card-body.

        getBoundingClientRect().height > 0 надёжнее CSS-классов и aria-атрибутов:
        работает при display:none (height=0), overflow:hidden и любом JS-фреймворке.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если card-body секции имеет высоту > 0 (видима пользователю).
        """
        return bool(
            self.page.evaluate(
                """(n) => {
                    const cards = document.querySelectorAll('.card');
                    if (!cards || cards.length < n) return false;
                    const card = cards[n - 1];
                    const body = card.querySelector('.card-body');
                    if (!body) return false;
                    return body.getBoundingClientRect().height > 0;
                }""",
                section_number,
            )
        )

    def click_section(self, section_number: int) -> "AccordionPage":
        """Кликнуть по триггеру секции для раскрытия/сворачивания.

        Ищет элемент с data-toggle/data-bs-toggle (Bootstrap 4/5),
        затем любую кнопку, затем сам card-header.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        self.page.evaluate(
            """(n) => {
                const cards = document.querySelectorAll('.card');
                if (!cards || cards.length < n) return;
                const card = cards[n - 1];
                const trigger =
                    card.querySelector('[data-toggle="collapse"]') ||
                    card.querySelector('[data-bs-toggle="collapse"]') ||
                    card.querySelector('.card-header button') ||
                    card.querySelector('.card-header');
                if (trigger) trigger.click();
            }""",
            section_number,
        )
        self.page.wait_for_timeout(600)
        return self

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
            Текст card-body секции или пустая строка.
        """
        try:
            text = self.page.evaluate(
                """(n) => {
                    const cards = document.querySelectorAll('.card');
                    if (!cards || cards.length < n) return '';
                    const body = cards[n - 1].querySelector('.card-body');
                    return body ? body.innerText : '';
                }""",
                section_number,
            )
            return str(text) if text else ""
        except Exception:
            return ""
