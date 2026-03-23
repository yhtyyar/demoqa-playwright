# DemoQA Playwright Automation

Фреймворк автоматизированного тестирования для [DemoQA](https://demoqa.com/) на базе **Playwright + Python + pytest**.

## Стек технологий

- **Python** 3.9+
- **Playwright** 1.42+
- **pytest** 8.0+
- **Faker** — генерация тестовых данных
- **pytest-html** — HTML-отчёты
- **allure-pytest** — отчёты Allure (опционально)

## Структура проекта

```text
demoqa-playwright/
├── conftest.py              # Глобальные фикстуры pytest
├── main.py                  # Точка входа для запуска
├── pytest.ini               # Конфигурация pytest
├── requirements.txt         # Зависимости
├── config/                  # Настройки и тестовые данные
│   ├── settings.py
│   └── test_data.py
├── pages/                   # Page Object Model
│   ├── base_page.py
│   ├── main_page.py
│   └── elements/
│       ├── text_box_page.py
│       ├── check_box_page.py
│       ├── radio_button_page.py
│       ├── buttons_page.py
│       └── web_tables_page.py
├── tests/                   # Тесты
│   ├── test_smoke.py
│   ├── test_elements.py
│   └── test_forms.py
├── utils/                   # Утилиты
│   ├── helpers.py
│   └── logger.py
├── docs/                    # Документация
│   ├── STYLE_GUIDE.md
│   ├── CONTRIBUTING.md
│   ├── test_plan.md
│   ├── test_cases.md
│   └── bug_report_template.md
└── reports/                 # Отчёты (автогенерация)
```

## Быстрый старт

### 1. Клонирование

```bash
git clone git@github.com:yhtyyar/demoqa-playwright.git
cd demoqa-playwright
```

### 2. Установка

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
playwright install
```

### 3. Настройка

Скопировать `.env.example` в `.env` и при необходимости отредактировать:

```bash
copy .env.example .env
```

### 4. Запуск тестов

```bash
# Smoke-тесты
pytest -m smoke

# Все тесты
pytest

# С HTML-отчётом
pytest --html=reports/html/report.html --self-contained-html

# В headed-режиме (с GUI браузера)
set HEADLESS=false && pytest -m smoke

# Через точку входа
python main.py
```

## Маркировка тестов

| Маркер       | Описание                         |
|--------------|----------------------------------|
| `smoke`      | Критический функционал (P0)      |
| `regression` | Основной функционал (P1)         |
| `ui`         | Валидация UI-элементов (P2)      |

## Документация

- [Руководство по стилю](docs/STYLE_GUIDE.md)
- [Руководство для контрибьюторов](docs/CONTRIBUTING.md)
- [Тест-план](docs/test_plan.md)
- [Тест-кейсы](docs/test_cases.md)
- [Шаблон баг-репорта](docs/bug_report_template.md)

## CI/CD

Проект включает GitHub Actions workflow для автоматического запуска тестов:

- **Push / PR** → smoke-тесты
- Отчёт сохраняется как артефакт
