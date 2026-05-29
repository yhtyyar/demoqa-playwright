"""Тесты для секции Alerts, Frame & Windows.

Эта секция демонстрирует уникальные возможности Playwright:
- Перехват browser dialog (alert/confirm/prompt) через page.on('dialog')
- Перехват новых вкладок/окон через context.expect_page()
- Работа с iframe через page.frame_locator() и цепочку вложенных frame_locator
- Работа с модальными окнами Bootstrap
"""

import pytest
from playwright.sync_api import Page

from pages.alerts_frame_windows.alerts_page import AlertsPage
from pages.alerts_frame_windows.browser_windows_page import BrowserWindowsPage
from pages.alerts_frame_windows.frames_page import FramesPage, NestedFramesPage
from pages.alerts_frame_windows.modal_dialogs_page import ModalDialogsPage


class TestAlerts:
    """Тесты для страницы Alerts — browser dialog handling."""

    @pytest.mark.smoke
    def test_simple_alert_shows_message(self, page: Page) -> None:
        """TC-A01: Простой alert — принять и проверить сообщение."""
        alerts = AlertsPage(page).open()

        message = alerts.accept_alert_and_get_message()

        assert message != "", "Alert не вернул сообщение"
        assert "alert" in message.lower() or len(message) > 0, \
            f"Неожиданное сообщение alert: '{message}'"

    @pytest.mark.regression
    def test_confirm_dialog_accepted(self, page: Page) -> None:
        """TC-A02: Confirm-диалог — принять (OK) и проверить результат."""
        alerts = AlertsPage(page).open()

        alerts.confirm_dialog(accept=True)

        result = alerts.get_confirm_result()
        assert "Ok" in result, f"Ожидался 'Ok' в результате, получен: '{result}'"

    @pytest.mark.regression
    def test_confirm_dialog_dismissed(self, page: Page) -> None:
        """TC-A03: Confirm-диалог — отклонить (Cancel) и проверить результат."""
        alerts = AlertsPage(page).open()

        alerts.confirm_dialog(accept=False)

        result = alerts.get_confirm_result()
        assert "Cancel" in result, f"Ожидался 'Cancel' в результате, получен: '{result}'"

    @pytest.mark.regression
    def test_prompt_with_text_input(self, page: Page) -> None:
        """TC-A04: Prompt-диалог — ввести текст и проверить результат."""
        alerts = AlertsPage(page).open()
        test_text = "Playwright Test Input"

        alerts.fill_prompt_and_accept(test_text)

        result = alerts.get_prompt_result()
        assert test_text in result, \
            f"Введённый текст '{test_text}' не найден в результате: '{result}'"

    @pytest.mark.regression
    @pytest.mark.slow
    def test_timer_alert_appears_after_delay(self, page: Page) -> None:
        """TC-A05: Timer alert — появляется через 5 секунд."""
        alerts = AlertsPage(page).open()

        message = alerts.accept_timer_alert()

        assert message != "", "Timer alert не вернул сообщение (не появился за 6 сек)"


class TestBrowserWindows:
    """Тесты для страницы Browser Windows — новые вкладки и окна."""

    @pytest.mark.smoke
    def test_new_tab_opens_with_correct_content(self, page: Page) -> None:
        """TC-BW01: Открытие новой вкладки — контент корректен."""
        browser_windows = BrowserWindowsPage(page).open()

        text = browser_windows.open_new_tab_and_get_text()

        assert "This is a sample page" in text, \
            f"Неожиданный текст на новой вкладке: '{text}'"

    @pytest.mark.regression
    def test_new_window_opens_with_correct_content(self, page: Page) -> None:
        """TC-BW02: Открытие нового окна — контент корректен."""
        browser_windows = BrowserWindowsPage(page).open()

        text = browser_windows.open_new_window_and_get_text()

        assert "This is a sample page" in text, \
            f"Неожиданный текст в новом окне: '{text}'"

    @pytest.mark.regression
    def test_original_page_stays_active_after_new_tab(self, page: Page) -> None:
        """Исходная вкладка остаётся активной после открытия новой."""
        browser_windows = BrowserWindowsPage(page).open()

        browser_windows.open_new_tab_and_get_text()

        assert "browser-windows" in page.url, \
            "URL исходной страницы изменился после открытия новой вкладки"


class TestFrames:
    """Тесты для страницы Frames — работа с iframe."""

    @pytest.mark.smoke
    def test_frame1_has_correct_text(self, page: Page) -> None:
        """TC-F01: Первый фрейм содержит ожидаемый текст."""
        frames = FramesPage(page).open()

        text = frames.get_frame1_text()

        assert "This is a sample page" in text, \
            f"Неожиданный текст в frame1: '{text}'"

    @pytest.mark.regression
    def test_frame2_has_correct_text(self, page: Page) -> None:
        """TC-F02: Второй фрейм содержит ожидаемый текст."""
        frames = FramesPage(page).open()

        text = frames.get_frame2_text()

        assert "This is a sample page" in text, \
            f"Неожиданный текст в frame2: '{text}'"

    @pytest.mark.regression
    def test_both_frames_load_independently(self, page: Page) -> None:
        """Оба фрейма загружаются и содержат текст независимо друг от друга."""
        frames = FramesPage(page).open()

        text1 = frames.get_frame1_text()
        text2 = frames.get_frame2_text()

        assert text1 != "", "Frame1 пустой"
        assert text2 != "", "Frame2 пустой"
        assert text1 == text2, \
            f"Ожидался одинаковый контент в обоих фреймах: '{text1}' vs '{text2}'"


class TestNestedFrames:
    """Тесты для страницы Nested Frames — вложенные iframe."""

    @pytest.mark.smoke
    def test_parent_frame_has_content(self, page: Page) -> None:
        """TC-NF01: Родительский фрейм содержит текст."""
        nested = NestedFramesPage(page).open()

        text = nested.get_parent_frame_text()

        assert "Parent frame" in text, \
            f"Текст 'Parent frame' не найден в родительском фрейме: '{text}'"

    @pytest.mark.regression
    def test_child_frame_has_content(self, page: Page) -> None:
        """TC-NF02: Дочерний фрейм внутри родительского содержит текст."""
        nested = NestedFramesPage(page).open()

        text = nested.get_child_frame_text()

        assert "Child Iframe" in text, \
            f"Текст 'Child Iframe' не найден в дочернем фрейме: '{text}'"


class TestModalDialogs:
    """Тесты для страницы Modal Dialogs — Bootstrap модальные окна."""

    @pytest.mark.smoke
    def test_small_modal_opens_and_closes(self, page: Page) -> None:
        """TC-MD01: Маленькое модальное окно открывается и закрывается."""
        modal = ModalDialogsPage(page).open()

        modal.open_small_modal()
        assert modal.is_modal_open(), "Маленькое модальное окно не открылось"
        title = modal.get_modal_title()
        assert "Small Modal" in title, f"Неожиданный заголовок: '{title}'"

        modal.close_small_modal()
        assert not modal.is_modal_open(), "Маленькое модальное окно не закрылось"

    @pytest.mark.regression
    def test_large_modal_opens_and_closes(self, page: Page) -> None:
        """TC-MD02: Большое модальное окно открывается, содержит текст, закрывается."""
        modal = ModalDialogsPage(page).open()

        modal.open_large_modal()
        assert modal.is_modal_open(), "Большое модальное окно не открылось"
        title = modal.get_modal_title()
        assert "Large Modal" in title, f"Неожиданный заголовок: '{title}'"
        body = modal.get_modal_body_text()
        assert len(body) > 50, "Тело большого модального окна слишком короткое"

        modal.close_large_modal()
        assert not modal.is_modal_open(), "Большое модальное окно не закрылось"

    @pytest.mark.regression
    def test_small_modal_body_content(self, page: Page) -> None:
        """Тело маленького модального окна содержит ожидаемый текст."""
        modal = ModalDialogsPage(page).open()

        modal.open_small_modal()

        body = modal.get_modal_body_text()
        assert "small modal" in body.lower(), \
            f"Неожиданный контент тела: '{body}'"
