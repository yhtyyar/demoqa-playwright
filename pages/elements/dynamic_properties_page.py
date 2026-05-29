"""Страница Dynamic Properties — элементы с отложенным появлением и изменением свойств."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class DynamicPropertiesPage(BasePage):
    """Page Object для страницы https://demoqa.com/dynamic-properties.

    Три кнопки с динамическим поведением (появляются/активируются через 5 сек).
    Демонстрирует стратегии ожидания Playwright: wait_for + state polling.

    Ключевой сценарий для портфолио — показывает, что тесты умеют
    работать с асинхронной логикой без sleep().
    """

    BUTTON_ENABLE_AFTER = "#enableAfter"
    BUTTON_COLOR_CHANGE = "#colorChange"
    BUTTON_VISIBLE_AFTER = "#visibleAfter"

    DYNAMIC_WAIT_MS = 6000

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "DynamicPropertiesPage":
        """Открыть страницу Dynamic Properties."""
        super().open("/dynamic-properties")
        return self

    @property
    def enable_after_button(self) -> Locator:
        """Кнопка, активирующаяся через 5 секунд."""
        return self.page.locator(self.BUTTON_ENABLE_AFTER)

    @property
    def color_change_button(self) -> Locator:
        """Кнопка, меняющая цвет через 5 секунд."""
        return self.page.locator(self.BUTTON_COLOR_CHANGE)

    @property
    def visible_after_button(self) -> Locator:
        """Кнопка, появляющаяся через 5 секунд."""
        return self.page.locator(self.BUTTON_VISIBLE_AFTER)

    def is_enable_button_enabled(self) -> bool:
        """Проверить, активна ли кнопка enableAfter прямо сейчас."""
        return self.is_enabled(self.enable_after_button)

    def wait_for_button_enabled(self) -> "DynamicPropertiesPage":
        """Ждать активации кнопки enableAfter (до 7 секунд).

        Returns:
            Экземпляр DynamicPropertiesPage для chaining.
        """
        self.enable_after_button.wait_for(state="visible", timeout=self.DYNAMIC_WAIT_MS + 1000)
        self.page.wait_for_function(
            "() => !document.querySelector('#enableAfter').disabled",
            timeout=self.DYNAMIC_WAIT_MS + 1000,
        )
        return self

    def get_color_change_button_color(self) -> str:
        """Получить текущий CSS-цвет кнопки colorChange.

        Returns:
            CSS-цвет кнопки в формате 'rgb(...)'.
        """
        return self.page.evaluate(
            """() => {
                const btn = document.querySelector('#colorChange');
                return window.getComputedStyle(btn).color;
            }"""
        )

    def wait_for_visible_button(self) -> "DynamicPropertiesPage":
        """Ждать появления кнопки visibleAfter (до 7 секунд).

        Returns:
            Экземпляр DynamicPropertiesPage для chaining.
        """
        self.visible_after_button.wait_for(state="visible", timeout=self.DYNAMIC_WAIT_MS + 1000)
        return self

    def is_visible_after_button_present(self) -> bool:
        """Проверить, присутствует ли кнопка visibleAfter в DOM."""
        return self.page.locator(self.BUTTON_VISIBLE_AFTER).count() > 0
