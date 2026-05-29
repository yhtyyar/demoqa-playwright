"""Страница Accordian — раскрывающиеся панели."""

from playwright.sync_api import Page

from pages.base_page import BasePage

# Заголовки секций как стабильные текстовые якоря (не зависят от HTML-структуры)
SECTION_TITLES = {
    1: "What is Lorem Ipsum?",
    2: "Where does it come from?",
    3: "Why do we use it?",
}


class AccordionPage(BasePage):
    """Page Object для страницы https://demoqa.com/accordian.

    Факты из CI-наблюдений:
      - .card count = 0           → нет Bootstrap .card
      - #section1Heading count = 0 → нет этих ID
      - aria-expanded не работает  → нет Bootstrap JS attrs
      → Используем text-based navigation: заголовки секций стабильны по тексту.
    """

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AccordionPage":
        """Открыть страницу Accordian."""
        super().open("/accordian")
        return self

    def click_section(self, section_number: int) -> "AccordionPage":
        """Кликнуть по заголовку секции через текстовый поиск.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            Экземпляр AccordionPage для chaining.
        """
        title = SECTION_TITLES[section_number]
        self.page.evaluate(
            """(title) => {
                // Ищем элемент содержащий этот текст
                const elements = [...document.querySelectorAll('*')].filter(
                    el => el.children.length === 0 && el.textContent.trim() === title
                );
                if (elements.length > 0) {
                    // Кликаем по кликабельному предку
                    let el = elements[0];
                    for (let i = 0; i < 5 && el; i++) {
                        if (['button', 'h5', 'h4', 'h3', 'a'].includes(el.tagName.toLowerCase())) {
                            el.click();
                            return;
                        }
                        el = el.parentElement;
                    }
                    // Если не нашли кнопку — кликаем по тексту
                    elements[0].click();
                }
            }""",
            title,
        )
        self.page.wait_for_timeout(600)
        return self

    def is_section_open(self, section_number: int) -> bool:
        """Проверить открытость секции через высоту контента после заголовка.

        Args:
            section_number: Номер секции (1, 2 или 3).

        Returns:
            True если контент секции видим (высота > 0).
        """
        title = SECTION_TITLES[section_number]
        return bool(
            self.page.evaluate(
                """(title) => {
                    const elements = [...document.querySelectorAll('*')].filter(
                        el => el.children.length === 0 && el.textContent.trim() === title
                    );
                    if (elements.length === 0) return false;
                    // Поднимаемся до контейнера с сиблингом-контентом
                    let el = elements[0].parentElement;
                    for (let i = 0; i < 6 && el; i++) {
                        const sibling = el.nextElementSibling;
                        if (sibling) {
                            const h = sibling.getBoundingClientRect().height;
                            if (h > 5) return true;   // секция открыта
                            if (h >= 0) return false;  // секция закрыта
                        }
                        el = el.parentElement;
                    }
                    return false;
                }""",
                title,
            )
        )

    def ensure_section_open(self, section_number: int) -> "AccordionPage":
        """Гарантировать открытость секции.

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
            Текст контента секции.
        """
        title = SECTION_TITLES[section_number]
        try:
            text = self.page.evaluate(
                """(title) => {
                    const elements = [...document.querySelectorAll('*')].filter(
                        el => el.children.length === 0 && el.textContent.trim() === title
                    );
                    if (elements.length === 0) return '';
                    let el = elements[0].parentElement;
                    for (let i = 0; i < 6 && el; i++) {
                        const sibling = el.nextElementSibling;
                        if (sibling) return sibling.innerText || '';
                        el = el.parentElement;
                    }
                    return '';
                }""",
                title,
            )
            return str(text).strip() if text else ""
        except Exception:
            return ""
