# Руководство для контрибьюторов

## Начало работы

### Вариант A: Docker (рекомендуется)

1. Клонировать репозиторий:

   ```bash
   git clone git@github.com:yhtyyar/demoqa-playwright.git
   cd demoqa-playwright
   ```

2. Запустить тесты через Docker Compose:

   ```bash
   docker compose run --rm smoke
   ```

### Вариант B: Локальная установка

1. Клонировать репозиторий:

   ```bash
   git clone git@github.com:yhtyyar/demoqa-playwright.git
   cd demoqa-playwright
   ```

2. Создать виртуальное окружение:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. Скопировать `.env.example` в `.env` и настроить переменные:

   ```bash
   cp .env.example .env
   ```

## Запуск тестов

### Через Docker Compose

```bash
# Smoke-тесты
docker compose run --rm smoke

# Regression-тесты
docker compose run --rm regression

# Конкретный браузер
docker compose run --rm tests-firefox
```

### Локально

```bash
# Smoke-тесты
pytest -m smoke

# Все тесты
pytest

# С HTML-отчётом
pytest --html=reports/html/report.html --self-contained-html

# В headed-режиме (с GUI браузера)
HEADLESS=false pytest
```

## Перед коммитом

1. Убедиться, что smoke-тесты проходят (`docker compose run --rm smoke` или `pytest -m smoke`)
2. Следовать [Руководству по стилю](STYLE_GUIDE.md)
3. Использовать формат коммитов: `<тип>(<область>): <описание>`

## Добавление нового Page Object

1. Создать файл в `pages/` или `pages/elements/`
2. Наследовать от `BasePage`
3. Определить локаторы как константы класса
4. Реализовать `open()`, свойства, действия, валидацию
5. Добавить тесты в `tests/`

## Добавление новых тестов

1. Создать метод в соответствующем тестовом классе
2. Добавить маркировку (`@pytest.mark.smoke` / `regression` / `ui`)
3. Следовать структуре Arrange → Act → Assert
4. Сообщения assert — на русском языке
