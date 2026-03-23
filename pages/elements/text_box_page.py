"""Страница TextBox — ввод текстовых данных."""

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class TextBoxPage(BasePage):
    """Page Object для страницы https://demoqa.com/text-box."""

    # --- Локаторы: поля ввода ---
    INPUT_FULL_NAME = "#userName"
    INPUT_EMAIL = "#userEmail"
    INPUT_CURRENT_ADDRESS = "#currentAddress"
    INPUT_PERMANENT_ADDRESS = "#permanentAddress"
    BUTTON_SUBMIT = "#submit"

    # --- Локаторы: блок результата ---
    OUTPUT_CONTAINER = "#output"
    OUTPUT_NAME = "#output #name"
    OUTPUT_EMAIL = "#output #email"
    OUTPUT_CURRENT_ADDRESS = "#output #currentAddress"
    OUTPUT_PERMANENT_ADDRESS = "#output #permanentAddress"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "TextBoxPage":
        """Открыть страницу TextBox."""
        super().open("/text-box")
        return self

    # --- Свойства ---

    @property
    def full_name_field(self) -> Locator:
        """Поле 'Full Name'."""
        return self.page.locator(self.INPUT_FULL_NAME)

    @property
    def email_field(self) -> Locator:
        """Поле 'Email'."""
        return self.page.locator(self.INPUT_EMAIL)

    @property
    def current_address_field(self) -> Locator:
        """Поле 'Current Address'."""
        return self.page.locator(self.INPUT_CURRENT_ADDRESS)

    @property
    def permanent_address_field(self) -> Locator:
        """Поле 'Permanent Address'."""
        return self.page.locator(self.INPUT_PERMANENT_ADDRESS)

    @property
    def submit_button(self) -> Locator:
        """Кнопка 'Submit'."""
        return self.page.locator(self.BUTTON_SUBMIT)

    @property
    def output_container(self) -> Locator:
        """Блок вывода результата."""
        return self.page.locator(self.OUTPUT_CONTAINER)

    # --- Действия ---

    def fill_form(
        self,
        name: str,
        email: str,
        current_addr: str,
        permanent_addr: str,
    ) -> "TextBoxPage":
        """Заполнить все поля формы.

        Args:
            name: Полное имя.
            email: Email-адрес.
            current_addr: Текущий адрес.
            permanent_addr: Постоянный адрес.

        Returns:
            Экземпляр TextBoxPage для chaining.
        """
        self.fill(self.full_name_field, name)
        self.fill(self.email_field, email)
        self.fill(self.current_address_field, current_addr)
        self.fill(self.permanent_address_field, permanent_addr)
        return self

    def submit(self) -> "TextBoxPage":
        """Нажать кнопку Submit."""
        self.scroll_to_element(self.submit_button)
        self.click(self.submit_button)
        return self

    def submit_and_wait(self) -> "TextBoxPage":
        """Нажать Submit и дождаться появления блока результата."""
        self.submit()
        self.wait_for_element(self.output_container)
        return self

    # --- Валидация ---

    def get_output_name(self) -> str:
        """Получить имя из блока результата."""
        return self.get_text(self.page.locator(self.OUTPUT_NAME))

    def get_output_email(self) -> str:
        """Получить email из блока результата."""
        return self.get_text(self.page.locator(self.OUTPUT_EMAIL))

    def get_output_current_address(self) -> str:
        """Получить текущий адрес из блока результата."""
        return self.get_text(self.page.locator(self.OUTPUT_CURRENT_ADDRESS))

    def get_output_permanent_address(self) -> str:
        """Получить постоянный адрес из блока результата."""
        return self.get_text(self.page.locator(self.OUTPUT_PERMANENT_ADDRESS))

    def is_output_visible(self) -> bool:
        """Проверить видимость блока результата."""
        return self.is_visible(self.output_container)
