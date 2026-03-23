# DemoQA Playwright Automation

[![DemoQA Tests](https://github.com/yhtyyar/demoqa-playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/yhtyyar/demoqa-playwright/actions/workflows/tests.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-1.42-green?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Docker](https://img.shields.io/badge/Docker-ready-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Фреймворк автоматизированного тестирования для [DemoQA](https://demoqa.com/) на базе **Playwright + Python + pytest + Docker**.

## Стек технологий

| Технология         | Назначение                |
|--------------------|---------------------------|
| **Python** 3.9+    | Язык программирования     |
| **Playwright**     | Браузерная автоматизация  |
| **pytest**         | Тестовый фреймворк        |
| **Docker**         | Контейнеризация и CI/CD   |
| **Faker**          | Генерация тестовых данных |
| **pytest-html**    | HTML-отчёты               |
| **GitHub Actions** | Непрерывная интеграция    |

## Структура проекта

```text
demoqa-playwright/
├── Dockerfile               # Docker-образ для тестов
├── docker-compose.yml       # Сервисы: smoke, regression, браузеры
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
├── .github/workflows/       # CI/CD
│   └── tests.yml
└── reports/                 # Отчёты (автогенерация, .gitignore)
```

## Быстрый старт

### Вариант 1: Docker (рекомендуется)

Не требует установки Python, Playwright или браузеров на хост-машину.

```bash
git clone git@github.com:yhtyyar/demoqa-playwright.git
cd demoqa-playwright

# Smoke-тесты
docker compose run --rm smoke

# Regression-тесты (все)
docker compose run --rm regression

# Тесты в конкретном браузере
docker compose run --rm tests-chromium
docker compose run --rm tests-firefox
docker compose run --rm tests-webkit
```

Отчёты сохраняются в `reports/html/` на хост-машине.

### Вариант 2: Локальная установка

```bash
git clone git@github.com:yhtyyar/demoqa-playwright.git
cd demoqa-playwright

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/macOS

pip install -r requirements.txt
playwright install

copy .env.example .env         # Windows
# cp .env.example .env         # Linux/macOS
```

### Запуск тестов (локально)

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

## Docker

### Сборка образа

```bash
docker build -t demoqa-tests .
```

### Запуск контейнера

```bash
# Smoke-тесты (по умолчанию)
docker run --rm -v ./reports:/app/reports demoqa-tests

# Все тесты
docker run --rm -v ./reports:/app/reports demoqa-tests -v --html=reports/html/report.html --self-contained-html

# С выбором маркера
docker run --rm -v ./reports:/app/reports demoqa-tests -m regression -v

# С выбором браузера
docker run --rm -e BROWSER=firefox -v ./reports:/app/reports demoqa-tests
```

### Docker Compose — сервисы

| Сервис           | Движок   | Покрытие браузеров                    |
|------------------|----------|---------------------------------------|
| `smoke`          | Blink    | Smoke-тесты (Chromium)                |
| `regression`     | Blink    | Полный regression (Chromium)          |
| `tests-chromium` | Blink    | Google Chrome, Яндекс Браузер, Edge   |
| `tests-firefox`  | Gecko    | Mozilla Firefox                       |
| `tests-webkit`   | WebKit   | Safari (macOS / iOS)                  |

## Кросс-браузерное тестирование

Playwright поддерживает 3 движка, покрывающих все основные браузеры:

| Движок     | Env `BROWSER` | Какие браузеры покрывает                         |
|------------|---------------|--------------------------------------------------|
| **Blink**  | `chromium`    | Google Chrome, Яндекс Браузер, Microsoft Edge    |
| **Gecko**  | `firefox`     | Mozilla Firefox                                  |
| **WebKit** | `webkit`      | Safari (macOS, iOS)                              |

```bash
# Запуск на конкретном движке (локально)
BROWSER=firefox pytest -m smoke

# Запуск реального Google Chrome (через channel)
BROWSER=chromium BROWSER_CHANNEL=chrome pytest -m smoke

# Все 3 движка через Docker Compose
docker compose run --rm tests-chromium
docker compose run --rm tests-firefox
docker compose run --rm tests-webkit
```

## Маркировка тестов

| Маркер       | Описание                         |
|--------------|----------------------------------|
| `smoke`      | Критический функционал (P0)      |
| `regression` | Основной функционал (P1)         |
| `ui`         | Валидация UI-элементов (P2)      |

## CI/CD Pipeline

Проект использует **GitHub Actions** с Docker-контейнеризацией.

### Архитектура пайплайна

```text
push / PR                      schedule (nightly)
    │                                │
    ▼                                ▼
┌──────────┐                  ┌──────────┐
│   Lint   │                  │   Lint   │
└────┬─────┘                  └────┬─────┘
     ▼                             ▼
┌──────────┐                  ┌──────────┐
│  Build   │ Docker image     │  Build   │
└────┬─────┘                  └────┬─────┘
     ▼                             ▼
┌──────────┐                  ┌──────────┐
│  Smoke   │                  │  Smoke   │
└────┬─────┘                  └────┬─────┘
     │                             ▼
     │                   ┌─────────┼─────────┐
     │                   ▼         ▼         ▼
     │              Chromium   Firefox    WebKit
     │                   │         │         │
     ▼                   └─────────┼─────────┘
┌──────────┐                       ▼
│  Report  │◄──────────────── ┌──────────┐
└──────────┘                  │  Report  │
                              └──────────┘
```

### Триггеры

| Событие                  | Что запускается                                          |
|--------------------------|----------------------------------------------------------|
| **Push** (main/develop)  | Lint → Build → Smoke → Report                            |
| **Pull Request**         | Lint → Build → Smoke → Report                            |
| **Nightly** (02:00 UTC)  | Lint → Build → Smoke → Regression (3 браузера) → Report  |
| **Manual dispatch**      | Настраиваемый маркер тестов                              |

### Артефакты

После каждого запуска CI сохраняются:

- **HTML-отчёты** — интерактивные отчёты pytest-html
- **JUnit XML** — результаты в формате JUnit (для интеграций)
- **Скриншоты** — снимки экрана при падении тестов

Отчёты доступны во вкладке **Actions → выбрать запуск → Artifacts**.

## Документация

- [Руководство по стилю](docs/STYLE_GUIDE.md)
- [Руководство для контрибьюторов](docs/CONTRIBUTING.md)
- [Тест-план](docs/test_plan.md)
- [Тест-кейсы](docs/test_cases.md)
- [Шаблон баг-репорта](docs/bug_report_template.md)
