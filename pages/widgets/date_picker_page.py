"""Страница Date Picker — выбор даты и даты+времени."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class DatePickerPage(BasePage):
    """Page Object для страницы https://demoqa.com/date-picker.

    Два контрола: простой Date Picker и Date+Time Picker (react-datepicker).
    Заполнение через прямой ввод в input — надёжнее, чем клики по календарю.
    """

    INPUT_DATE = "#datePickerMonthYearInput"
    INPUT_DATETIME = "#dateAndTimePickerInput"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "DatePickerPage":
        """Открыть страницу Date Picker."""
        super().open("/date-picker")
        return self

    @property
    def date_input(self) -> Locator:
        """Поле ввода даты (Select Date)."""
        return self.page.locator(self.INPUT_DATE)

    @property
    def datetime_input(self) -> Locator:
        """Поле ввода даты и времени."""
        return self.page.locator(self.INPUT_DATETIME)

    def set_date(self, date_str: str) -> "DatePickerPage":
        """Установить дату через прямой ввод в поле.

        Args:
            date_str: Дата в формате MM/DD/YYYY (например, '05/15/2025').

        Returns:
            Экземпляр DatePickerPage для chaining.
        """
        self.date_input.click()
        self.date_input.triple_click()
        self.date_input.type(date_str)
        self.page.keyboard.press("Tab")
        return self

    def set_datetime(self, datetime_str: str) -> "DatePickerPage":
        """Установить дату и время.

        Args:
            datetime_str: Дата+время в формате 'May 15, 2025 10:00 AM'.

        Returns:
            Экземпляр DatePickerPage для chaining.
        """
        self.datetime_input.click()
        self.datetime_input.triple_click()
        self.datetime_input.type(datetime_str)
        self.page.keyboard.press("Tab")
        return self

    def get_date_value(self) -> str:
        """Получить текущее значение поля Date.

        Returns:
            Значение атрибута value поля ввода даты.
        """
        return self.get_attribute(self.date_input, "value") or ""

    def get_datetime_value(self) -> str:
        """Получить текущее значение поля Date+Time.

        Returns:
            Значение атрибута value поля ввода даты и времени.
        """
        return self.get_attribute(self.datetime_input, "value") or ""
