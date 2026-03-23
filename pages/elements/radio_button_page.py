"""Страница RadioButton — выбор радиокнопок."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class RadioButtonPage(BasePage):
    """Page Object для страницы https://demoqa.com/radio-button."""

    # --- Локаторы ---
    RADIO_YES = "label[for='yesRadio']"
    RADIO_IMPRESSIVE = "label[for='impressiveRadio']"
    RADIO_NO = "label[for='noRadio']"
    RESULT_TEXT = ".mt-3 .text-success"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "RadioButtonPage":
        """Открыть страницу RadioButton."""
        super().open("/radio-button")
        return self

    # --- Свойства ---

    @property
    def yes_radio(self) -> Locator:
        """Радиокнопка 'Yes'."""
        return self.page.locator(self.RADIO_YES)

    @property
    def impressive_radio(self) -> Locator:
        """Радиокнопка 'Impressive'."""
        return self.page.locator(self.RADIO_IMPRESSIVE)

    @property
    def no_radio(self) -> Locator:
        """Радиокнопка 'No'."""
        return self.page.locator(self.RADIO_NO)

    @property
    def result_text(self) -> Locator:
        """Текст результата выбора."""
        return self.page.locator(self.RESULT_TEXT)

    # --- Геттеры ---

    def get_radio_by_name(self, option: str) -> Locator:
        """Получить локатор радиокнопки по названию опции.

        Args:
            option: Название опции ('Yes', 'Impressive', 'No').

        Returns:
            Локатор label радиокнопки.
        """
        options_map = {
            "Yes": self.RADIO_YES,
            "Impressive": self.RADIO_IMPRESSIVE,
            "No": self.RADIO_NO,
        }
        return self.page.locator(options_map[option])

    # --- Действия ---

    def select_yes(self) -> "RadioButtonPage":
        """Выбрать опцию 'Yes'."""
        self.click(self.yes_radio)
        return self

    def select_impressive(self) -> "RadioButtonPage":
        """Выбрать опцию 'Impressive'."""
        self.click(self.impressive_radio)
        return self

    def select_by_name(self, option: str) -> "RadioButtonPage":
        """Выбрать радиокнопку по названию опции.

        Args:
            option: Название опции ('Yes', 'Impressive', 'No').

        Returns:
            Экземпляр RadioButtonPage для chaining.
        """
        self.click(self.get_radio_by_name(option))
        return self

    # --- Валидация ---

    def get_result_text(self) -> str:
        """Получить текст результата выбора.

        Returns:
            Текст с результатом (например, 'Yes', 'Impressive').
        """
        return self.get_text(self.result_text)

    def is_radio_visible(self, option: str) -> bool:
        """Проверить видимость радиокнопки.

        Args:
            option: Название опции.

        Returns:
            True если элемент видим.
        """
        return self.is_visible(self.get_radio_by_name(option))

    def is_no_radio_disabled(self) -> bool:
        """Проверить, что радиокнопка 'No' заблокирована.

        Returns:
            True если кнопка 'No' заблокирована.
        """
        return self.page.locator("#noRadio").is_disabled()
