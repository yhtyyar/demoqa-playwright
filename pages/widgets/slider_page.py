"""Страница Slider — ползунок диапазона."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class SliderPage(BasePage):
    """Page Object для страницы https://demoqa.com/slider."""

    INPUT_SLIDER = ".range-slider input[type='range']"
    INPUT_VALUE = "#sliderValue"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "SliderPage":
        """Открыть страницу Slider."""
        super().open("/slider")
        return self

    @property
    def slider(self) -> Locator:
        """Ползунок range input."""
        return self.page.locator(self.INPUT_SLIDER)

    @property
    def value_input(self) -> Locator:
        """Поле отображения текущего значения."""
        return self.page.locator(self.INPUT_VALUE)

    def set_value(self, value: int) -> "SliderPage":
        """Установить значение ползунка через JavaScript.

        Прямое изменение value + dispatch input event — надёжнее
        drag-эмуляции, которая зависит от пикселей и масштаба.

        Args:
            value: Числовое значение от 0 до 100.

        Returns:
            Экземпляр SliderPage для chaining.
        """
        self.page.evaluate(
            """(val) => {
                const slider = document.querySelector('.range-slider input[type="range"]');
                slider.value = val;
                slider.dispatchEvent(new Event('input', { bubbles: true }));
                slider.dispatchEvent(new Event('change', { bubbles: true }));
            }""",
            value,
        )
        self.page.wait_for_timeout(300)
        return self

    def get_value(self) -> int:
        """Получить текущее числовое значение из поля-индикатора.

        Returns:
            Числовое значение ползунка.
        """
        raw = self.get_attribute(self.value_input, "value") or "0"
        return int(raw)
