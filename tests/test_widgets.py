"""Тесты для секции Widgets.

Covers: Accordian, Date Picker, Slider.

Стратегия для accordion: DemoQA — внешний сайт, начальное состояние нестабильно.
  smoke   → только загрузка страницы (всегда проходит)
  regression → функциональность открытия/закрытия (через ensure_section_open)
"""

import pytest
from playwright.sync_api import Page

from pages.widgets.accordion_page import AccordionPage
from pages.widgets.date_picker_page import DatePickerPage
from pages.widgets.slider_page import SliderPage


class TestAccordion:
    """Тесты для страницы Accordian."""

    @pytest.mark.smoke
    def test_accordion_page_loads(self, page: Page) -> None:
        """TC-W01: Страница аккордеона загружается и содержит секции."""
        AccordionPage(page).open()

        # Проверяем только что страница загрузилась с секциями — не трогаем состояние
        card_count = page.locator(".card").count()
        assert card_count >= 3, f"Ожидалось 3+ секции, найдено: {card_count}"

    @pytest.mark.regression
    def test_section1_can_be_opened(self, page: Page) -> None:
        """TC-W02: Первая секция открывается по клику."""
        accordion = AccordionPage(page).open()

        accordion.ensure_section_open(1)

        assert accordion.is_section_open(1), "Секция 1 не открылась"

    @pytest.mark.regression
    def test_section2_can_be_opened(self, page: Page) -> None:
        """TC-W03: Вторая секция открывается по клику."""
        accordion = AccordionPage(page).open()

        # Закрываем 2 если открыта, затем открываем — гарантируем состояние
        if accordion.is_section_open(2):
            accordion.click_section(2)
        accordion.click_section(2)

        assert accordion.is_section_open(2), "Секция 2 не открылась"

    @pytest.mark.regression
    def test_section3_can_be_opened(self, page: Page) -> None:
        """TC-W04: Третья секция открывается по клику."""
        accordion = AccordionPage(page).open()

        if accordion.is_section_open(3):
            accordion.click_section(3)
        accordion.click_section(3)

        assert accordion.is_section_open(3), "Секция 3 не открылась"

    @pytest.mark.regression
    def test_section1_content_has_text(self, page: Page) -> None:
        """Открытая секция 1 содержит непустой текст."""
        accordion = AccordionPage(page).open()

        accordion.ensure_section_open(1)
        text = accordion.get_section_text(1)

        assert len(text.strip()) > 20, f"Текст первой секции слишком короткий: '{text[:50]}'"

    @pytest.mark.regression
    def test_open_section_can_be_closed(self, page: Page) -> None:
        """Открытая секция закрывается повторным кликом."""
        accordion = AccordionPage(page).open()

        accordion.ensure_section_open(1)
        assert accordion.is_section_open(1), "ensure_section_open не открыл секцию 1"

        accordion.click_section(1)

        assert not accordion.is_section_open(1), "Секция 1 не закрылась после клика"


class TestDatePicker:
    """Тесты для страницы Date Picker."""

    @pytest.mark.smoke
    def test_date_input_is_visible(self, page: Page) -> None:
        """TC-DP01: Поле выбора даты присутствует на странице."""
        date_picker = DatePickerPage(page).open()

        assert date_picker.is_visible(date_picker.date_input), "Поле Date Input не отображается"
        assert date_picker.is_visible(date_picker.datetime_input), "Поле Date+Time Input не отображается"

    @pytest.mark.regression
    def test_set_date_value(self, page: Page) -> None:
        """TC-DP02: Установить дату и проверить значение в поле."""
        date_picker = DatePickerPage(page).open()

        date_picker.set_date("05/15/2025")

        value = date_picker.get_date_value()
        assert "05/15/2025" in value, f"Ожидаемая дата '05/15/2025' не установлена. Текущее значение: '{value}'"

    @pytest.mark.regression
    def test_date_field_has_default_value(self, page: Page) -> None:
        """Поле даты имеет значение по умолчанию при открытии страницы."""
        date_picker = DatePickerPage(page).open()

        value = date_picker.get_date_value()

        assert value != "", "Поле даты пустое при открытии страницы"

    @pytest.mark.ui
    def test_datetime_field_has_default_value(self, page: Page) -> None:
        """Поле Date+Time имеет значение по умолчанию при открытии страницы."""
        date_picker = DatePickerPage(page).open()

        value = date_picker.get_datetime_value()

        assert value != "", "Поле Date+Time пустое при открытии страницы"


class TestSlider:
    """Тесты для страницы Slider."""

    @pytest.mark.smoke
    def test_slider_is_visible(self, page: Page) -> None:
        """TC-S01: Ползунок присутствует на странице."""
        slider = SliderPage(page).open()

        assert slider.is_visible(slider.slider), "Ползунок не отображается"

    @pytest.mark.regression
    def test_set_slider_to_value(self, page: Page) -> None:
        """TC-S02: Установить значение ползунка и проверить индикатор."""
        slider = SliderPage(page).open()

        slider.set_value(75)

        assert slider.get_value() == 75, f"Ожидалось значение 75, получено: {slider.get_value()}"

    @pytest.mark.regression
    def test_slider_min_value(self, page: Page) -> None:
        """Ползунок принимает минимальное значение 0."""
        slider = SliderPage(page).open()

        slider.set_value(0)

        assert slider.get_value() == 0, f"Ожидалось 0, получено: {slider.get_value()}"

    @pytest.mark.regression
    def test_slider_max_value(self, page: Page) -> None:
        """Ползунок принимает максимальное значение 100."""
        slider = SliderPage(page).open()

        slider.set_value(100)

        assert slider.get_value() == 100, f"Ожидалось 100, получено: {slider.get_value()}"

    @pytest.mark.regression
    def test_slider_has_default_value(self, page: Page) -> None:
        """Ползунок имеет значение по умолчанию при открытии страницы."""
        slider = SliderPage(page).open()

        value = slider.get_value()

        assert 0 <= value <= 100, f"Значение по умолчанию {value} вне диапазона [0, 100]"
