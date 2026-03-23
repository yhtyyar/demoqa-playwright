"""Тесты для секции Forms."""

import pytest
from playwright.sync_api import Page

from config.test_data import TestData


class TestPracticeForm:
    """Тесты для страницы Practice Form."""

    @pytest.mark.regression
    def test_submit_practice_form(self, page: Page) -> None:
        """Заполнение и отправка формы Practice Form."""
        # Arrange
        data = TestData.PRACTICE_FORM_DATA
        page.goto("https://demoqa.com/automation-practice-form")

        # Удалить рекламные баннеры
        page.evaluate(
            """() => {
                const ads = document.querySelectorAll(
                    '#fixedban, .ad, #adplus-anchor, iframe[id^="google_ads"]'
                );
                ads.forEach(ad => ad.remove());
                document.querySelector('footer')?.remove();
            }"""
        )

        # Act — заполнить основные поля
        page.locator("#firstName").fill(data["first_name"])
        page.locator("#lastName").fill(data["last_name"])
        page.locator("#userEmail").fill(data["email"])

        # Выбрать пол (Male)
        page.locator("label[for='gender-radio-1']").click()

        # Ввести номер телефона
        page.locator("#userNumber").fill(data["mobile"])

        # Ввести текущий адрес
        page.locator("#currentAddress").fill(data["address"])

        # Нажать Submit
        page.locator("#submit").scroll_into_view_if_needed()
        page.locator("#submit").click()

        # Assert — проверить модальное окно с результатами
        modal = page.locator(".modal-content")
        modal.wait_for(state="visible", timeout=10000)

        modal_text = modal.text_content() or ""
        assert data["first_name"] in modal_text, \
            f"Имя '{data['first_name']}' не найдено в модальном окне"
        assert data["last_name"] in modal_text, \
            f"Фамилия '{data['last_name']}' не найдена в модальном окне"
        assert data["email"] in modal_text, \
            f"Email '{data['email']}' не найден в модальном окне"

    @pytest.mark.ui
    def test_form_fields_visible(self, page: Page) -> None:
        """Проверка видимости основных полей формы Practice Form."""
        # Arrange
        page.goto("https://demoqa.com/automation-practice-form")

        # Assert
        assert page.locator("#firstName").is_visible(), "Поле First Name не видно"
        assert page.locator("#lastName").is_visible(), "Поле Last Name не видно"
        assert page.locator("#userEmail").is_visible(), "Поле Email не видно"
        assert page.locator("#userNumber").is_visible(), "Поле Mobile не видно"
        assert page.locator("#submit").is_visible(), "Кнопка Submit не видна"
