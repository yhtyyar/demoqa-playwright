"""Страница Buttons — проверка типов кликов."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class ButtonsPage(BasePage):
    """Page Object для страницы https://demoqa.com/buttons."""

    # --- Локаторы: кнопки ---
    BUTTON_DOUBLE_CLICK = "#doubleClickBtn"
    BUTTON_RIGHT_CLICK = "#rightClickBtn"
    BUTTON_CLICK = "//button[text()='Click Me']"

    # --- Локаторы: сообщения ---
    MESSAGE_DOUBLE_CLICK = "#doubleClickMessage"
    MESSAGE_RIGHT_CLICK = "#rightClickMessage"
    MESSAGE_CLICK = "#dynamicClickMessage"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "ButtonsPage":
        """Открыть страницу Buttons."""
        super().open("/buttons")
        return self

    # --- Свойства ---

    @property
    def double_click_button(self) -> Locator:
        """Кнопка для двойного клика."""
        return self.page.locator(self.BUTTON_DOUBLE_CLICK)

    @property
    def right_click_button(self) -> Locator:
        """Кнопка для правого клика."""
        return self.page.locator(self.BUTTON_RIGHT_CLICK)

    @property
    def click_button(self) -> Locator:
        """Кнопка для обычного клика."""
        return self.page.locator(self.BUTTON_CLICK)

    # --- Действия ---

    def perform_double_click(self) -> "ButtonsPage":
        """Выполнить двойной клик по кнопке.

        Returns:
            Экземпляр ButtonsPage для chaining.
        """
        self.double_click_button.dblclick(timeout=5000)
        return self

    def perform_right_click(self) -> "ButtonsPage":
        """Выполнить правый клик по кнопке.

        Returns:
            Экземпляр ButtonsPage для chaining.
        """
        self.right_click_button.click(button="right", timeout=5000)
        return self

    def perform_click(self) -> "ButtonsPage":
        """Выполнить обычный клик по кнопке.

        Returns:
            Экземпляр ButtonsPage для chaining.
        """
        self.click(self.click_button)
        return self

    # --- Валидация ---

    def get_double_click_message(self) -> str:
        """Получить сообщение после двойного клика."""
        return self.get_text(self.page.locator(self.MESSAGE_DOUBLE_CLICK))

    def get_right_click_message(self) -> str:
        """Получить сообщение после правого клика."""
        return self.get_text(self.page.locator(self.MESSAGE_RIGHT_CLICK))

    def get_click_message(self) -> str:
        """Получить сообщение после обычного клика."""
        return self.get_text(self.page.locator(self.MESSAGE_CLICK))
