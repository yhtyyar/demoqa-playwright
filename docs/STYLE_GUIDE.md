# Руководство по стилю кода — DemoQA Automation

## 1. Общие принципы

- **Язык кода:** Python 3.9+
- **Язык комментариев и документации:** русский
- **Форматирование:** PEP 8, максимальная длина строки — 120 символов
- **Именование файлов:** `snake_case.py`

## 2. Именование

| Элемент            | Стиль            | Пример                       |
|--------------------|------------------|------------------------------|
| Модули / файлы     | `snake_case`     | `text_box_page.py`           |
| Классы             | `PascalCase`     | `TextBoxPage`                |
| Методы / функции   | `snake_case`     | `fill_form()`                |
| Константы          | `UPPER_SNAKE`    | `BASE_URL`                   |
| Локаторы (CSS/XPath)| `UPPER_SNAKE`   | `INPUT_FULL_NAME`            |
| Фикстуры pytest    | `snake_case`     | `def page(browser):`         |
| Тестовые классы    | `Test` + `PascalCase` | `TestTextBox`           |
| Тестовые методы    | `test_` + `snake_case` | `test_submit_valid_data` |

## 3. Структура Page Object

```python
"""Краткое описание страницы."""

from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class ExamplePage(BasePage):
    """Описание Page Object."""

    # --- Локаторы (константы класса) ---
    INPUT_NAME = "#name"
    BUTTON_SUBMIT = "#submit"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> "ExamplePage":
        """Открыть страницу."""
        return super().open("/example")

    # --- Свойства (геттеры локаторов) ---
    @property
    def name_field(self) -> Locator:
        return self.page.locator(self.INPUT_NAME)

    # --- Действия ---
    def fill_name(self, name: str) -> "ExamplePage":
        """Заполнить поле имени."""
        self.fill(self.name_field, name)
        return self

    # --- Валидация ---
    def get_output_name(self) -> str:
        """Получить имя из результата."""
        return self.get_text(self.page.locator("#output"))
```

### Порядок секций в Page Object:
1. Docstring модуля
2. Импорты
3. Локаторы (константы)
4. `__init__`
5. `open`
6. Свойства (`@property`) — геттеры локаторов
7. Действия (методы взаимодействия)
8. Валидация (методы проверки)

## 4. Структура теста

```python
@pytest.mark.smoke
def test_descriptive_name(self, page):
    """TC-XXX: Описание тест-кейса."""
    # Arrange
    page_object = PageObject(page).open()

    # Act
    page_object.perform_action()

    # Assert
    assert condition, "Понятное сообщение об ошибке на русском"
```

### Правила тестов:
- Каждый тест — независимый и идемпотентный
- Структура: **Arrange → Act → Assert**
- Assert-сообщения — на русском, чётко описывают проблему
- Маркировка: `@pytest.mark.smoke`, `@pytest.mark.regression`, `@pytest.mark.ui`

## 5. Импорты

Порядок (по PEP 8):
1. Стандартная библиотека
2. Сторонние пакеты
3. Локальные модули

```python
import os
from pathlib import Path

import pytest
from playwright.sync_api import Page

from pages.base_page import BasePage
from config.settings import Settings
```

## 6. Docstrings

- Все публичные классы и методы — обязательно
- Формат: Google-style

```python
def fill_form(self, name: str, email: str) -> "TextBoxPage":
    """Заполнить форму.

    Args:
        name: Полное имя пользователя.
        email: Email пользователя.

    Returns:
        Экземпляр TextBoxPage для chaining.
    """
```

## 7. Type Hints

- Обязательны для всех публичных методов
- Возвращаемый тип `-> "ClassName"` для method chaining
- `Optional[str]` вместо `str | None`

## 8. Обработка ожиданий

- **Запрещено:** `time.sleep()`
- **Рекомендуется:** `locator.wait_for()`, `page.wait_for_selector()`, `expect()`
- Таймауты — из `Settings`, не хардкод

## 9. Git-коммиты

### Формат:
```
<тип>(<область>): <описание>
```

### Типы:
| Тип        | Назначение                          |
|------------|-------------------------------------|
| `feat`     | Новая функциональность              |
| `fix`      | Исправление бага                    |
| `docs`     | Документация                        |
| `style`    | Форматирование (без изменения логики)|
| `refactor` | Рефакторинг                         |
| `test`     | Добавление / изменение тестов       |
| `chore`    | Обслуживание, зависимости, CI       |

### Примеры:
```
feat(pages): добавить TextBoxPage с методами заполнения формы
test(elements): добавить smoke-тесты для TextBox
docs(project): создать тест-план и тест-кейсы
fix(conftest): исправить скриншот при падении теста
chore(deps): обновить playwright до 1.42.0
```

### Правила:
- Описание на русском языке
- Первая буква описания — строчная
- Без точки в конце
- Максимум 72 символа в первой строке

## 10. Ветвление Git

| Ветка           | Назначение              |
|-----------------|-------------------------|
| `main`          | Стабильная версия       |
| `develop`       | Разработка              |
| `feature/<имя>` | Новая функциональность  |
| `fix/<имя>`     | Исправление             |
