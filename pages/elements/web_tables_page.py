"""Страница Web Tables — работа с таблицей данных."""

from typing import Dict, List, Optional

from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class WebTablesPage(BasePage):
    """Page Object для страницы https://demoqa.com/webtables."""

    # --- Локаторы: кнопки ---
    BUTTON_ADD = "#addNewRecordButton"
    BUTTON_SUBMIT = "#submit"
    INPUT_SEARCH = "#searchBox"

    # --- Локаторы: форма регистрации ---
    INPUT_FIRST_NAME = "#firstName"
    INPUT_LAST_NAME = "#lastName"
    INPUT_EMAIL = "#userEmail"
    INPUT_AGE = "#age"
    INPUT_SALARY = "#salary"
    INPUT_DEPARTMENT = "#department"

    # --- Локаторы: таблица (стандартная HTML table) ---
    TABLE_ROWS = "tbody tr"
    TABLE_CELL = "td"
    EDIT_BUTTON = "[title='Edit']"
    DELETE_BUTTON = "[title='Delete']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "WebTablesPage":
        """Открыть страницу Web Tables."""
        super().open("/webtables")
        return self

    # --- Свойства ---

    @property
    def add_button(self) -> Locator:
        """Кнопка 'Add' для добавления записи."""
        return self.page.locator(self.BUTTON_ADD)

    @property
    def submit_button(self) -> Locator:
        """Кнопка 'Submit' в форме."""
        return self.page.locator(self.BUTTON_SUBMIT)

    @property
    def search_box(self) -> Locator:
        """Поле поиска."""
        return self.page.locator(self.INPUT_SEARCH)

    # --- Действия ---

    def click_add(self) -> "WebTablesPage":
        """Нажать кнопку добавления новой записи."""
        self.click(self.add_button)
        return self

    def fill_registration_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        age: str,
        salary: str,
        department: str,
    ) -> "WebTablesPage":
        """Заполнить форму регистрации.

        Args:
            first_name: Имя.
            last_name: Фамилия.
            email: Email-адрес.
            age: Возраст.
            salary: Зарплата.
            department: Отдел.

        Returns:
            Экземпляр WebTablesPage для chaining.
        """
        self.fill(self.page.locator(self.INPUT_FIRST_NAME), first_name)
        self.fill(self.page.locator(self.INPUT_LAST_NAME), last_name)
        self.fill(self.page.locator(self.INPUT_EMAIL), email)
        self.fill(self.page.locator(self.INPUT_AGE), age)
        self.fill(self.page.locator(self.INPUT_SALARY), salary)
        self.fill(self.page.locator(self.INPUT_DEPARTMENT), department)
        return self

    def submit_form(self) -> "WebTablesPage":
        """Нажать кнопку Submit в форме."""
        self.click(self.submit_button)
        self.page.wait_for_timeout(1000)
        return self

    def search(self, query: str) -> "WebTablesPage":
        """Выполнить поиск по таблице.

        Args:
            query: Поисковый запрос.

        Returns:
            Экземпляр WebTablesPage для chaining.
        """
        self.fill(self.search_box, query)
        self.page.wait_for_timeout(500)
        return self

    def delete_row_by_index(self, index: int) -> "WebTablesPage":
        """Удалить строку по индексу.

        Args:
            index: Индекс строки (0-based).

        Returns:
            Экземпляр WebTablesPage для chaining.
        """
        delete_btn = self.page.locator(f"tbody tr:nth-child({index + 1}) {self.DELETE_BUTTON}")
        self.click(delete_btn)
        return self

    # --- Валидация ---

    def get_all_rows_data(self) -> List[Dict[str, str]]:
        """Получить данные всех непустых строк таблицы.

        Returns:
            Список словарей с данными строк.
        """
        return self.page.evaluate("""() => {
            const rows = document.querySelectorAll('tbody tr');
            const data = [];
            rows.forEach(row => {
                const cells = row.querySelectorAll('td');
                if (cells.length >= 6) {
                    const firstName = (cells[0].textContent || '').trim();
                    if (firstName) {
                        data.push({
                            first_name: firstName,
                            last_name: (cells[1].textContent || '').trim(),
                            age: (cells[2].textContent || '').trim(),
                            email: (cells[3].textContent || '').trim(),
                            salary: (cells[4].textContent || '').trim(),
                            department: (cells[5].textContent || '').trim(),
                        });
                    }
                }
            });
            return data;
        }""")

    def find_row_by_email(self, email: str) -> Optional[int]:
        """Найти индекс строки по email.

        Args:
            email: Email для поиска.

        Returns:
            Индекс строки или None если не найдена.
        """
        rows_data = self.get_all_rows_data()
        for i, row in enumerate(rows_data):
            if row["email"] == email:
                return i
        return None

    def is_record_exists(self, email: str) -> bool:
        """Проверить существование записи по email.

        Args:
            email: Email для проверки.

        Returns:
            True если запись найдена.
        """
        return self.find_row_by_email(email) is not None

    def get_row_count(self) -> int:
        """Получить количество непустых строк таблицы.

        Returns:
            Количество строк с данными.
        """
        return len(self.get_all_rows_data())
