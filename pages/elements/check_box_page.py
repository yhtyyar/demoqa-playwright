"""Страница CheckBox — работа с деревом чекбоксов (rc-tree)."""

from typing import List

from playwright.sync_api import Locator, Page

from config.settings import Settings
from pages.base_page import BasePage


class CheckBoxPage(BasePage):
    """Page Object для страницы https://demoqa.com/checkbox.

    DemoQA использует rc-tree (Ant Design) для дерева чекбоксов.
    Глобальных кнопок Expand All/Collapse All нет —
    каждый узел имеет свой .rc-tree-switcher.
    """

    # --- Локаторы (rc-tree) ---
    TREE = ".rc-tree"
    TREE_NODE = ".rc-tree-treenode"
    SWITCHER_CLOSED = ".rc-tree-switcher_close"
    SWITCHER_OPEN = ".rc-tree-switcher_open"
    CHECKBOX = ".rc-tree-checkbox"
    NODE_TITLE = ".rc-tree-title"
    RESULT_CONTAINER = "#result"
    RESULT_ITEMS = "#result .text-success"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "CheckBoxPage":
        """Открыть страницу CheckBox."""
        super().open("/checkbox")
        self.page.locator(self.TREE).wait_for(
            state="visible", timeout=Settings.EXPECT_TIMEOUT,
        )
        return self

    # --- Свойства ---

    @property
    def result_container(self) -> Locator:
        """Блок вывода результата."""
        return self.page.locator(self.RESULT_CONTAINER)

    # --- Геттеры локаторов ---

    def get_checkbox_label(self, item_name: str) -> Locator:
        """Получить кликабельный label чекбокса по имени элемента.

        Args:
            item_name: Имя элемента в дереве (например, 'Desktop', 'Notes').

        Returns:
            Локатор label-элемента.
        """
        return self.page.locator(
            f".rc-tree-title:text-is('{item_name}')"
        ).first

    def get_toggle_icon(self, item_name: str) -> Locator:
        """Получить иконку раскрытия/сворачивания для узла дерева.

        Args:
            item_name: Имя узла дерева.

        Returns:
            Локатор иконки toggle.
        """
        return self.page.locator(
            f".rc-tree-treenode:has(.rc-tree-title:text-is('{item_name}'))"
            f" >> .rc-tree-switcher"
        )

    # --- Действия ---

    def expand_all(self) -> "CheckBoxPage":
        """Развернуть все узлы дерева (кликая по каждому закрытому switcher)."""
        while True:
            closed = self.page.locator(self.SWITCHER_CLOSED)
            if closed.count() == 0:
                break
            closed.first.click(force=True, timeout=Settings.ACTION_TIMEOUT)
            self.page.wait_for_timeout(300)
        return self

    def collapse_all(self) -> "CheckBoxPage":
        """Свернуть все узлы дерева (кликая по каждому открытому switcher)."""
        while True:
            opened = self.page.locator(self.SWITCHER_OPEN)
            if opened.count() == 0:
                break
            opened.first.click(force=True, timeout=Settings.ACTION_TIMEOUT)
            self.page.wait_for_timeout(300)
        return self

    def toggle_item(self, item_name: str) -> "CheckBoxPage":
        """Развернуть или свернуть узел дерева.

        Args:
            item_name: Имя узла дерева.

        Returns:
            Экземпляр CheckBoxPage для chaining.
        """
        toggle = self.get_toggle_icon(item_name)
        if toggle.count() > 0:
            toggle.click(force=True, timeout=Settings.ACTION_TIMEOUT)
        return self

    def check_item(self, item_name: str) -> "CheckBoxPage":
        """Отметить чекбокс по имени элемента.

        Args:
            item_name: Имя элемента для выбора.

        Returns:
            Экземпляр CheckBoxPage для chaining.
        """
        checkbox = self.page.locator(
            f".rc-tree-treenode:has(.rc-tree-title:text-is('{item_name}'))"
            f" >> .rc-tree-checkbox"
        )
        checkbox.click(force=True, timeout=Settings.ACTION_TIMEOUT)
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
