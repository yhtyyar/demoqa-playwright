"""Страница Alerts — браузерные диалоговые окна."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class AlertsPage(BasePage):
    """Page Object для страницы https://demoqa.com/alerts.

    Демонстрирует работу с browser alert/confirm/prompt через
    Playwright dialog handler — уникальная возможность фреймворка.
    """

    BUTTON_ALERT = "#alertButton"
    BUTTON_TIMER_ALERT = "#timerAlertButton"
    BUTTON_CONFIRM = "#confirmButton"
    BUTTON_PROMPT = "#promtButton"
    RESULT_CONFIRM = "#confirmResult"
    RESULT_PROMPT = "#promptResult"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "AlertsPage":
        """Открыть страницу Alerts."""
        super().open("/alerts")
        return self

    @property
    def confirm_result(self) -> Locator:
        """Блок результата подтверждения."""
        return self.page.locator(self.RESULT_CONFIRM)

    @property
    def prompt_result(self) -> Locator:
        """Блок результата ввода в prompt."""
        return self.page.locator(self.RESULT_PROMPT)

    def click_simple_alert(self) -> "AlertsPage":
        """Нажать кнопку простого alert (без ожидания — alert появляется сразу)."""
        self.click(self.page.locator(self.BUTTON_ALERT))
        return self

    def click_timer_alert(self) -> "AlertsPage":
        """Нажать кнопку alert с таймером (появляется через 5 секунд)."""
        self.click(self.page.locator(self.BUTTON_TIMER_ALERT))
        return self

    def click_confirm_alert(self) -> "AlertsPage":
        """Нажать кнопку confirm-диалога."""
        self.click(self.page.locator(self.BUTTON_CONFIRM))
        return self

    def click_prompt_alert(self) -> "AlertsPage":
        """Нажать кнопку prompt-диалога."""
        self.click(self.page.locator(self.BUTTON_PROMPT))
        return self

    def accept_alert_and_get_message(self) -> str:
        """Принять alert и вернуть его сообщение.

        Регистрирует одноразовый handler до клика — Playwright требует,
        чтобы dialog handler был установлен до того, как dialog откроется.

        Returns:
            Текст сообщения в alert.
        """
        message_holder: list[str] = []

        def handle_dialog(dialog):
            message_holder.append(dialog.message)
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click_simple_alert()
        self.page.wait_for_timeout(500)
        return message_holder[0] if message_holder else ""

    def accept_timer_alert(self) -> str:
        """Принять timer alert и вернуть сообщение (ждёт до 10 сек)."""
        message_holder: list[str] = []

        def handle_dialog(dialog):
            message_holder.append(dialog.message)
            dialog.accept()

        self.page.once("dialog", handle_dialog)
        self.click_timer_alert()
        self.page.wait_for_timeout(6000)
        return message_holder[0] if message_holder else ""

    def confirm_dialog(self, accept: bool = True) -> "AlertsPage":
        """Принять или отклонить confirm-диалог.

        Args:
            accept: True — OK, False — Cancel.

        Returns:
            Экземпляр AlertsPage для chaining.
        """

        def handle_dialog(dialog):
            if accept:
                dialog.accept()
            else:
                dialog.dismiss()

        self.page.once("dialog", handle_dialog)
        self.click_confirm_alert()
        self.page.wait_for_timeout(500)
        return self

    def fill_prompt_and_accept(self, text: str) -> "AlertsPage":
        """Ввести текст в prompt и принять.

        Args:
            text: Текст для ввода в prompt.

        Returns:
            Экземпляр AlertsPage для chaining.
        """

        def handle_dialog(dialog):
            dialog.accept(text)

        self.page.once("dialog", handle_dialog)
        self.click_prompt_alert()
        self.page.wait_for_timeout(500)
        return self

    def get_confirm_result(self) -> str:
        """Получить текст результата confirm-диалога."""
        self.wait_for_element(self.confirm_result)
        return self.get_text(self.confirm_result)

    def get_prompt_result(self) -> str:
        """Получить текст результата prompt-диалога."""
        self.wait_for_element(self.prompt_result)
        return self.get_text(self.prompt_result)
