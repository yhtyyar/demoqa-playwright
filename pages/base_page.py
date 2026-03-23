"""Базовый класс для всех страниц (Page Object Model)."""

from typing import Optional

from playwright.sync_api import Locator, Page, TimeoutError as PlaywrightTimeout

from config.settings import Settings
from utils.logger import logger


class BasePage:
    """Базовый класс Page Object Model.

    Предоставляет общие методы взаимодействия с элементами страницы.
    Все конкретные Page Object наследуются от этого класса.
    """

    def __init__(self, page: Page) -> None:
        self.page = page
        self.timeout = Settings.TIMEOUT

    def open(self, url_path: str) -> "BasePage":
        """Открыть страницу по относительному пути.

        Args:
            url_path: Относительный путь (например, '/text-box').

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        full_url = f"{Settings.BASE_URL}{url_path}"
        logger.info("Открытие страницы: %s", full_url)
        self.page.goto(full_url, timeout=Settings.PAGE_LOAD_TIMEOUT)
        return self

    # --- Действия ---

    def click(self, locator: Locator) -> "BasePage":
        """Кликнуть по элементу.

        Args:
            locator: Локатор элемента.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.click(timeout=Settings.ACTION_TIMEOUT)
        return self

    def fill(self, locator: Locator, text: str) -> "BasePage":
        """Заполнить поле ввода.

        Args:
            locator: Локатор поля ввода.
            text: Текст для ввода.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.fill(text, timeout=Settings.ACTION_TIMEOUT)
        return self

    def check(self, locator: Locator) -> "BasePage":
        """Отметить чекбокс.

        Args:
            locator: Локатор чекбокса.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.check(timeout=Settings.ACTION_TIMEOUT)
        return self

    def uncheck(self, locator: Locator) -> "BasePage":
        """Снять отметку чекбокса.

        Args:
            locator: Локатор чекбокса.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.uncheck(timeout=Settings.ACTION_TIMEOUT)
        return self

    def select_option(self, locator: Locator, value: str) -> "BasePage":
        """Выбрать опцию в выпадающем списке.

        Args:
            locator: Локатор выпадающего списка.
            value: Значение для выбора.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.select_option(value, timeout=Settings.ACTION_TIMEOUT)
        return self

    # --- Получение данных ---

    def get_text(self, locator: Locator) -> str:
        """Получить текстовое содержимое элемента.

        Args:
            locator: Локатор элемента.

        Returns:
            Текст элемента.
        """
        return locator.text_content(timeout=Settings.EXPECT_TIMEOUT) or ""

    def get_attribute(self, locator: Locator, attribute: str) -> Optional[str]:
        """Получить значение атрибута элемента.

        Args:
            locator: Локатор элемента.
            attribute: Имя атрибута.

        Returns:
            Значение атрибута или None.
        """
        return locator.get_attribute(attribute, timeout=Settings.EXPECT_TIMEOUT)

    # --- Проверки ---

    def is_visible(self, locator: Locator) -> bool:
        """Проверить видимость элемента.

        Args:
            locator: Локатор элемента.

        Returns:
            True если элемент видим, иначе False.
        """
        try:
            locator.wait_for(state="visible", timeout=Settings.EXPECT_TIMEOUT)
            return True
        except PlaywrightTimeout:
            return False

    def is_enabled(self, locator: Locator) -> bool:
        """Проверить доступность элемента для взаимодействия.

        Args:
            locator: Локатор элемента.

        Returns:
            True если элемент доступен, иначе False.
        """
        return locator.is_enabled()

    # --- Ожидания ---

    def wait_for_element(self, locator: Locator, state: str = "visible") -> "BasePage":
        """Ожидать элемент в определённом состоянии.

        Args:
            locator: Локатор элемента.
            state: Ожидаемое состояние ('visible', 'hidden', 'attached', 'detached').

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.wait_for(state=state, timeout=Settings.TIMEOUT)
        return self

    # --- Утилиты ---

    def screenshot(self, name: str) -> str:
        """Сделать скриншот текущей страницы.

        Args:
            name: Имя файла скриншота (без расширения).

        Returns:
            Путь к сохранённому скриншоту.
        """
        path = str(Settings.SCREENSHOTS_DIR / f"{name}.png")
        self.page.screenshot(path=path)
        logger.info("Скриншот сохранён: %s", path)
        return path

    def scroll_to_element(self, locator: Locator) -> "BasePage":
        """Прокрутить страницу до элемента.

        Args:
            locator: Локатор элемента.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        locator.scroll_into_view_if_needed(timeout=Settings.ACTION_TIMEOUT)
        return self

    def remove_ads(self) -> "BasePage":
        """Удалить рекламные баннеры со страницы DemoQA.

        Returns:
            Экземпляр текущего Page Object для chaining.
        """
        self.page.evaluate(
            """() => {
                const ads = document.querySelectorAll(
                    '#fixedban, .ad, #adplus-anchor, iframe[id^="google_ads"]'
                );
                ads.forEach(ad => ad.remove());
                document.querySelector('footer')?.remove();
            }"""
        )
        return self
