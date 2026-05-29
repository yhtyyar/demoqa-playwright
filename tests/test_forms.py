"""Тесты для секции Forms."""

import pytest
from playwright.sync_api import Page

from config.settings import Settings
from config.test_data import TestData


class TestPracticeForm:
    """Тесты для страницы Practice Form."""

    @pytest.mark.regression
    def test_submit_practice_form(self, page: Page) -> None:
        """Заполнение и отправка формы Practice Form."""
        # Arrange
        data = TestData.PRACTICE_FORM_DATA
        page.goto(
            f"{Settings.BASE_URL}/automation-practice-form",
            wait_until="domcontentloaded",
        )

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
        page.goto(
            f"{Settings.BASE_URL}/automation-practice-form",
            wait_until="domcontentloaded",
        )

        # Assert
        assert page.locator("#firstName").is_visible(), "Поле First Name не видно"
        assert page.locator("#lastName").is_visible(), "Поле Last Name не видно"
        assert page.locator("#userEmail").is_visible(), "Поле Email не видно"
        assert page.locator("#userNumber").is_visible(), "Поле Mobile не видно"
        assert page.locator("#submit").is_visible(), "Кнопка Submit не видна"

    @pytest.mark.regression
    def test_submit_without_required_fields(self, page: Page) -> None:
        """Отправка пустой формы — модальное окно не появляется."""
        # Arrange
        page.goto(
            f"{Settings.BASE_URL}/automation-practice-form",
            wait_until="domcontentloaded",
        )
        page.evaluate(
            """() => {
                const ads = document.querySelectorAll(
                    '#fixedban, .ad, #adplus-anchor, iframe[id^="google_ads"]'
                );
                ads.forEach(ad => ad.remove());
                document.querySelector('footer')?.remove();
            }"""
        )

        # Act
        page.locator("#submit").scroll_into_view_if_needed()
        page.locator("#submit").click()

        # Assert — форма не отправляется без обязательных полей
        modal = page.locator(".modal-content")
        is_modal_visible = modal.is_visible()
        assert not is_modal_visible, \
            "Форма принята без обязательных полей (First Name, Last Name, Mobile)"

    @pytest.mark.regression
    def test_gender_radio_buttons_present(self, page: Page) -> None:
        """Радиокнопки выбора пола присутствуют на форме."""
        # Arrange
        page.goto(
            f"{Settings.BASE_URL}/automation-practice-form",
            wait_until="domcontentloaded",
        )

        # Assert — три варианта пола
        for gender_id in ["gender-radio-1", "gender-radio-2", "gender-radio-3"]:
            label = page.locator(f"label[for='{gender_id}']")
            assert label.is_visible(), f"Радиокнопка {gender_id} не видна"

    @pytest.mark.regression
    def test_submit_with_gender_and_required_fields(self, page: Page) -> None:
        """Форма принимается с обязательными полями + выбором пола Female."""
        # Arrange
        data = TestData.PRACTICE_FORM_DATA
        page.goto(
            f"{Settings.BASE_URL}/automation-practice-form",
            wait_until="domcontentloaded",
        )
        page.evaluate(
            """() => {
                const ads = document.querySelectorAll(
                    '#fixedban, .ad, #adplus-anchor, iframe[id^="google_ads"]'
                );
                ads.forEach(ad => ad.remove());
                document.querySelector('footer')?.remove();
            }"""
        )

        # Act
        page.locator("#firstName").fill(data["first_name"])
        page.locator("#lastName").fill(data["last_name"])
        page.locator("#userEmail").fill(data["email"])
        # Выбор пола Female
        page.locator("label[for='gender-radio-2']").click()
        page.locator("#userNumber").fill(data["mobile"])
        page.locator("#submit").scroll_into_view_if_needed()
        page.locator("#submit").click()

        # Assert
        modal = page.locator(".modal-content")
        modal.wait_for(state="visible", timeout=10000)
        modal_text = modal.text_content() or ""
        assert data["first_name"] in modal_text, \
            f"Имя '{data['first_name']}' не найдено в модальном окне"
        assert "Female" in modal_text, \
            "Выбранный пол 'Female' не отображается в результате"
