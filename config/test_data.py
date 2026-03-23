"""Тестовые данные для DemoQA."""

from faker import Faker

fake = Faker()


class TestData:
    """Набор тестовых данных, генерируемых динамически."""

    # TextBox
    TEXTBOX_DATA: dict = {
        "full_name": fake.name(),
        "email": fake.email(),
        "current_address": fake.address().replace("\n", ", "),
        "permanent_address": fake.address().replace("\n", ", "),
    }

    # WebTable
    WEBTABLE_DATA: dict = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "age": str(fake.random_int(min=18, max=65)),
        "salary": str(fake.random_int(min=1000, max=10000)),
        "department": fake.random_element(
            ["Engineering", "Sales", "Marketing", "HR"]
        ),
    }

    # Practice Form
    PRACTICE_FORM_DATA: dict = {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "mobile": str(fake.random_int(min=1000000000, max=9999999999)),
        "subjects": ["Maths", "Physics"],
        "hobbies": ["Sports", "Reading"],
        "address": fake.address().replace("\n", ", "),
        "state": "NCR",
        "city": "Delhi",
    }

    # Ожидаемые сообщения
    EXPECTED_MESSAGES: dict = {
        "textbox": "Name, Email, Current Address, Permanent Address",
        "radio_yes": "Yes",
        "radio_impressive": "Impressive",
        "radio_no": "No",
        "button_click": "You have done a dynamic click",
        "button_double_click": "You have done a double click",
        "button_right_click": "You have done a right click",
    }
