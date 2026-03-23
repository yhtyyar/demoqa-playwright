"""Smoke-тесты — быстрая проверка критического функционала."""

import pytest
from playwright.sync_api import Page

from config.test_data import TestData
from pages.elements.buttons_page import ButtonsPage
from pages.elements.radio_button_page import RadioButtonPage
from pages.elements.text_box_page import TextBoxPage


class TestSmoke:
    """Набор smoke-тестов для быстрой валидации."""

    @pytest.mark.smoke
    def test_homepage_loads(self, page: Page) -> None:
        """Проверка загрузки главной страницы DemoQA."""
        # Act
        response = page.goto("https://demoqa.com")

        # Assert — проверяем HTTP-статус, URL и наличие ключевых элементов
        assert response is not None and response.ok, \
            f"Главная страница вернула ошибку: {response.status if response else 'нет ответа'}"
        assert "demoqa.com" in page.url, \
            f"URL не содержит 'demoqa.com': {page.url}"
        assert page.locator(".category-cards").is_visible(), \
            "Карточки категорий не отображаются на главной странице"

    @pytest.mark.smoke
    def test_textbox_basic_flow(self, page: Page) -> None:
        """Базовый поток: заполнение и отправка формы TextBox."""
        # Arrange
        text_box = TextBoxPage(page).open()

        # Act
        text_box.fill_form(
            name="Test User",
            email="test@test.com",
            current_addr="Address 1",
            permanent_addr="Address 2",
        ).submit_and_wait()

        # Assert
        assert text_box.is_output_visible(), "Блок результата не отображается после отправки формы"

    @pytest.mark.smoke
    def test_buttons_respond_to_click(self, page: Page) -> None:
        """Проверка реакции кнопки на обычный клик."""
        # Arrange
        buttons = ButtonsPage(page).open()

        # Act
        buttons.perform_click()

        # Assert
        message = buttons.get_click_message()
        assert message != "", "Сообщение после клика отсутствует"

    @pytest.mark.smoke
    def test_radio_button_selection(self, page: Page) -> None:
        """Проверка выбора радиокнопки 'Yes'."""
        # Arrange
        radio = RadioButtonPage(page).open()

        # Act
        radio.select_yes()

        # Assert
        result = radio.get_result_text()
        assert "Yes" in result, f"Ожидался текст 'Yes', получен: '{result}'"
