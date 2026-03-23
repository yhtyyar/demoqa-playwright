"""Страница CheckBox — работа с деревом чекбоксов."""

from typing import List

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CheckBoxPage(BasePage):
    """Page Object для страницы https://demoqa.com/checkbox."""

    # --- Локаторы ---
    EXPAND_ALL_BUTTON = "button[title='Expand all']"
    COLLAPSE_ALL_BUTTON = "button[title='Collapse all']"
    RESULT_CONTAINER = "#result"
    RESULT_ITEMS = "#result .text-success"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "CheckBoxPage":
        """Открыть страницу CheckBox."""
        super().open("/checkbox")
        return self

    # --- Свойства ---

    @property
    def result_container(self) -> Locator:
        """Блок вывода результата."""
        return self.page.locator(self.RESULT_CONTAINER)

    @property
    def expand_all_button(self) -> Locator:
        """Кнопка 'Развернуть всё'."""
        return self.page.locator(self.EXPAND_ALL_BUTTON)

    @property
    def collapse_all_button(self) -> Locator:
        """Кнопка 'Свернуть всё'."""
        return self.page.locator(self.COLLAPSE_ALL_BUTTON)

    # --- Геттеры локаторов ---

    def get_checkbox_label(self, item_name: str) -> Locator:
        """Получить кликабельный label чекбокса по имени элемента.

        Args:
            item_name: Имя элемента в дереве (например, 'Desktop', 'Notes').

        Returns:
            Локатор label-элемента.
        """
        return self.page.locator(
            f".rct-node-leaf .rct-title:has-text('{item_name}'), "
            f".rct-node-parent .rct-title:has-text('{item_name}')"
        ).first

    def get_toggle_icon(self, item_name: str) -> Locator:
        """Получить иконку раскрытия/сворачивания для узла дерева.

        Args:
            item_name: Имя узла дерева.

        Returns:
            Локатор иконки toggle.
        """
        return self.page.locator(
            f"//span[contains(@class, 'rct-title') and text()='{item_name}']"
            f"/ancestor::li[1]//button[contains(@class, 'rct-collapse')]"
        )

    # --- Действия ---

    def expand_all(self) -> "CheckBoxPage":
        """Развернуть все узлы дерева."""
        self.click(self.expand_all_button)
        return self

    def collapse_all(self) -> "CheckBoxPage":
        """Свернуть все узлы дерева."""
        self.click(self.collapse_all_button)
        return self

    def toggle_item(self, item_name: str) -> "CheckBoxPage":
        """Развернуть или свернуть узел дерева.

        Args:
            item_name: Имя узла дерева.

        Returns:
            Экземпляр CheckBoxPage для chaining.
        """
        toggle = self.get_toggle_icon(item_name)
        if toggle.is_visible():
            toggle.click()
        return self

    def check_item(self, item_name: str) -> "CheckBoxPage":
        """Отметить чекбокс по имени элемента.

        Args:
            item_name: Имя элемента для выбора.

        Returns:
            Экземпляр CheckBoxPage для chaining.
        """
        label = self.get_checkbox_label(item_name)
        label.click()
        return self

    # --- Валидация ---

    def get_selected_items(self) -> List[str]:
        """Получить список выбранных элементов из блока результата.

        Returns:
            Список имён выбранных элементов в нижнем регистре.
        """
        if not self.is_visible(self.result_container):
            return []
        items = self.page.locator(self.RESULT_ITEMS).all()
        return [item.text_content().lower() for item in items if item.text_content()]

    def is_result_visible(self) -> bool:
        """Проверить видимость блока результата."""
        return self.is_visible(self.result_container)
