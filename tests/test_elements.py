"""Тесты для секции Elements."""

import pytest
from playwright.sync_api import Page

from config.test_data import TestData
from pages.elements.buttons_page import ButtonsPage
from pages.elements.check_box_page import CheckBoxPage
from pages.elements.radio_button_page import RadioButtonPage
from pages.elements.text_box_page import TextBoxPage
from pages.elements.web_tables_page import WebTablesPage


class TestTextBox:
    """Тесты для страницы TextBox."""

    @pytest.mark.smoke
    def test_submit_with_valid_data(self, page: Page) -> None:
        """TC-001: Валидация формы TextBox с корректными данными."""
        # Arrange
        text_box = TextBoxPage(page).open()
        data = TestData.TEXTBOX_DATA

        # Act
        text_box.fill_form(
            name=data["full_name"],
            email=data["email"],
            current_addr=data["current_address"],
            permanent_addr=data["permanent_address"],
        ).submit_and_wait()

        # Assert
        assert text_box.is_output_visible(), "Блок результата не отображается"
        assert data["full_name"] in text_box.get_output_name(), f"Имя '{data['full_name']}' не найдено в результате"
        assert data["email"] in text_box.get_output_email(), f"Email '{data['email']}' не найден в результате"

    @pytest.mark.regression
    def test_submit_with_empty_fields(self, page: Page) -> None:
        """Отправка формы TextBox с пустыми полями — результат не должен появиться."""
        # Arrange
        text_box = TextBoxPage(page).open()

        # Act
        text_box.submit()

        # Assert
        assert not text_box.is_output_visible(), "Блок результата появился при отправке пустой формы"

    @pytest.mark.regression
    def test_submit_with_invalid_email(self, page: Page) -> None:
        """Отправка формы TextBox с некорректным email."""
        # Arrange
        text_box = TextBoxPage(page).open()

        # Act
        text_box.fill_form(
            name="Test User",
            email="invalid-email",
            current_addr="Address 1",
            permanent_addr="Address 2",
        ).submit()

        # Assert — при некорректном email поле подсвечивается ошибкой
        email_field = text_box.email_field
        border_class = text_box.get_attribute(email_field, "class") or ""
        # DemoQA добавляет класс field-error при невалидном email
        has_error = "field-error" in border_class or not text_box.is_output_visible()
        assert has_error, "Форма принята с невалидным email"

    @pytest.mark.ui
    def test_all_fields_visible(self, page: Page) -> None:
        """Проверка видимости всех полей формы TextBox."""
        # Arrange
        text_box = TextBoxPage(page).open()

        # Assert
        assert text_box.is_visible(text_box.full_name_field), "Поле Full Name не видно"
        assert text_box.is_visible(text_box.email_field), "Поле Email не видно"
        assert text_box.is_visible(text_box.current_address_field), "Поле Current Address не видно"
        assert text_box.is_visible(text_box.permanent_address_field), "Поле Permanent Address не видно"
        assert text_box.is_visible(text_box.submit_button), "Кнопка Submit не видна"


class TestCheckBox:
    """Тесты для страницы CheckBox."""

    @pytest.mark.regression
    def test_expand_all_and_check_item(self, page: Page) -> None:
        """TC-002: Развернуть дерево и выбрать элемент."""
        # Arrange
        check_box = CheckBoxPage(page).open()

        # Act
        check_box.expand_all()
        check_box.check_item("Notes")

        # Assert
        selected = check_box.get_selected_items()
        assert "notes" in selected, f"'notes' не найден в выбранных: {selected}"

    @pytest.mark.regression
    def test_check_parent_selects_children(self, page: Page) -> None:
        """Выбор родительского элемента выбирает все дочерние."""
        # Arrange
        check_box = CheckBoxPage(page).open()

        # Act
        check_box.expand_all()
        check_box.check_item("Desktop")

        # Assert
        selected = check_box.get_selected_items()
        assert "desktop" in selected, "'desktop' не в выбранных"
        assert "notes" in selected, "'notes' не в выбранных при выборе Desktop"
        assert "commands" in selected, "'commands' не в выбранных при выборе Desktop"

    @pytest.mark.ui
    def test_expand_collapse_buttons(self, page: Page) -> None:
        """Проверка работы кнопок Expand All / Collapse All."""
        # Arrange
        check_box = CheckBoxPage(page).open()

        # Act & Assert — развернуть
        check_box.expand_all()
        assert check_box.is_visible(check_box.get_checkbox_label("Notes")), "Элемент 'Notes' не виден после Expand All"

        # Act & Assert — свернуть
        check_box.collapse_all()
        assert not check_box.is_visible(
            check_box.get_checkbox_label("Notes")
        ), "Элемент 'Notes' всё ещё виден после Collapse All"


class TestRadioButton:
    """Тесты для страницы RadioButton."""

    @pytest.mark.smoke
    def test_select_impressive(self, page: Page) -> None:
        """TC-003: Выбор радиокнопки 'Impressive'."""
        # Arrange
        radio = RadioButtonPage(page).open()

        # Act
        radio.select_impressive()

        # Assert
        result = radio.get_result_text()
        assert "Impressive" in result, f"Ожидался 'Impressive', получен: '{result}'"

    @pytest.mark.regression
    def test_select_yes(self, page: Page) -> None:
        """Выбор радиокнопки 'Yes'."""
        # Arrange
        radio = RadioButtonPage(page).open()

        # Act
        radio.select_yes()

        # Assert
        result = radio.get_result_text()
        assert "Yes" in result, f"Ожидался 'Yes', получен: '{result}'"

    @pytest.mark.regression
    def test_no_radio_is_disabled(self, page: Page) -> None:
        """Радиокнопка 'No' должна быть заблокирована."""
        # Arrange
        radio = RadioButtonPage(page).open()

        # Assert
        assert radio.is_no_radio_disabled(), "Радиокнопка 'No' доступна, ожидалась заблокированной"

    @pytest.mark.ui
    def test_all_options_visible(self, page: Page) -> None:
        """Проверка видимости всех радиокнопок."""
        # Arrange
        radio = RadioButtonPage(page).open()

        # Assert
        assert radio.is_radio_visible("Yes"), "Опция 'Yes' не видна"
        assert radio.is_radio_visible("Impressive"), "Опция 'Impressive' не видна"
        assert radio.is_radio_visible("No"), "Опция 'No' не видна"


class TestButtons:
    """Тесты для страницы Buttons."""

    @pytest.mark.smoke
    def test_single_click(self, page: Page) -> None:
        """TC-005a: Проверка обычного клика."""
        # Arrange
        buttons = ButtonsPage(page).open()

        # Act
        buttons.perform_click()

        # Assert
        message = buttons.get_click_message()
        assert "dynamic click" in message.lower(), f"Неверное сообщение после клика: '{message}'"

    @pytest.mark.smoke
    def test_double_click(self, page: Page) -> None:
        """TC-005b: Проверка двойного клика."""
        # Arrange
        buttons = ButtonsPage(page).open()

        # Act
        buttons.perform_double_click()

        # Assert
        message = buttons.get_double_click_message()
        assert "double click" in message.lower(), f"Неверное сообщение после двойного клика: '{message}'"

    @pytest.mark.regression
    def test_right_click(self, page: Page) -> None:
        """TC-005c: Проверка правого клика."""
        # Arrange
        buttons = ButtonsPage(page).open()

        # Act
        buttons.perform_right_click()

        # Assert
        message = buttons.get_right_click_message()
        assert "right click" in message.lower(), f"Неверное сообщение после правого клика: '{message}'"

    @pytest.mark.regression
    def test_all_buttons_respond(self, page: Page) -> None:
        """Проверка всех трёх типов кликов за один тест."""
        # Arrange
        buttons = ButtonsPage(page).open()

        # Act & Assert — обычный клик
        buttons.perform_click()
        assert buttons.get_click_message() != "", "Нет сообщения после обычного клика"

        # Act & Assert — двойной клик
        buttons.perform_double_click()
        assert buttons.get_double_click_message() != "", "Нет сообщения после двойного клика"

        # Act & Assert — правый клик
        buttons.perform_right_click()
        assert buttons.get_right_click_message() != "", "Нет сообщения после правого клика"


class TestWebTables:
    """Тесты для страницы Web Tables."""

    @pytest.mark.regression
    def test_add_new_record(self, page: Page) -> None:
        """TC-004: Добавление новой записи в таблицу."""
        # Arrange
        table = WebTablesPage(page).open()
        data = TestData.WEBTABLE_DATA
        initial_count = table.get_row_count()

        # Act
        table.click_add()
        table.fill_registration_form(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            age=data["age"],
            salary=data["salary"],
            department=data["department"],
        ).submit_form()

        # Assert
        assert table.is_record_exists(data["email"]), f"Запись с email '{data['email']}' не найдена в таблице"
        assert table.get_row_count() == initial_count + 1, "Количество строк не увеличилось на 1"

    @pytest.mark.regression
    def test_search_record(self, page: Page) -> None:
        """Поиск записи в таблице."""
        # Arrange
        table = WebTablesPage(page).open()

        # Act — ищем по существующим данным (Cierra)
        table.search("Cierra")

        # Assert
        rows = table.get_all_rows_data()
        assert len(rows) >= 1, "Поиск не вернул результатов"
        assert any("Cierra" in row["first_name"] for row in rows), "Запись 'Cierra' не найдена в результатах поиска"

    @pytest.mark.ui
    def test_table_has_default_records(self, page: Page) -> None:
        """Проверка наличия предзаполненных записей в таблице."""
        # Arrange
        table = WebTablesPage(page).open()

        # Assert
        rows = table.get_all_rows_data()
        assert len(rows) >= 3, f"Ожидалось минимум 3 записи, найдено: {len(rows)}"

    @pytest.mark.regression
    def test_delete_record(self, page: Page) -> None:
        """TC-WT04: Удаление записи из таблицы уменьшает количество строк."""
        # Arrange
        table = WebTablesPage(page).open()
        initial_count = table.get_row_count()
        assert initial_count > 0, "Нет записей для удаления"

        # Act — удаляем первую строку
        table.delete_row_by_index(0)
        table.page.wait_for_timeout(500)

        # Assert
        new_count = table.get_row_count()
        assert new_count == initial_count - 1, f"Ожидалось {initial_count - 1} строк, найдено: {new_count}"

    @pytest.mark.regression
    def test_edit_existing_record(self, page: Page) -> None:
        """TC-WT05: Редактирование существующей записи через кнопку Edit."""
        # Arrange
        table = WebTablesPage(page).open()

        # Act — открыть форму редактирования первой строки
        table.page.locator("tbody tr:nth-child(1) [title='Edit']").click()
        form_visible = table.page.locator("#registration-form-modal").is_visible()

        # Assert
        assert form_visible, "Форма редактирования не открылась"

        # Изменить salary
        salary_field = table.page.locator("#salary")
        salary_field.triple_click()
        salary_field.fill("99999")
        table.page.locator("#submit").click()
        table.page.wait_for_timeout(500)

        rows = table.get_all_rows_data()
        assert any(row["salary"] == "99999" for row in rows), "Изменённое значение salary не сохранилось в таблице"

    @pytest.mark.regression
    def test_search_clears_result(self, page: Page) -> None:
        """Очистка поля поиска восстанавливает все записи."""
        # Arrange
        table = WebTablesPage(page).open()
        initial_count = table.get_row_count()

        # Act — поиск по несуществующему значению
        table.search("XXXXXXXXXX_NOTEXIST")
        assert table.get_row_count() == 0, "Поиск должен был вернуть 0 результатов"

        # Очистить поиск
        table.search("")
        table.page.wait_for_timeout(500)

        # Assert
        restored_count = table.get_row_count()
        assert (
            restored_count == initial_count
        ), f"После очистки поиска ожидалось {initial_count} строк, найдено: {restored_count}"
