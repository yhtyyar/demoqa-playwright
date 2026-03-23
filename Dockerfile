FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

LABEL maintainer="yhtyyar"
LABEL description="DemoQA Playwright Automation Framework"

WORKDIR /app

# Установка зависимостей (кэшируется отдельным слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание директорий для отчётов с открытыми правами (для volume mount)
RUN mkdir -p reports/html reports/xml reports/screenshots reports/allure \
    && chmod -R 777 reports

# Пользователь без root-прав (безопасность)
RUN groupadd -r tester && useradd -r -g tester -d /home/tester -s /bin/bash tester \
    && mkdir -p /home/tester \
    && chown -R tester:tester /app /home/tester
USER tester

# Переменные окружения по умолчанию
ENV BASE_URL=https://demoqa.com \
    BROWSER=chromium \
    BROWSER_CHANNEL="" \
    HEADLESS=true \
    TIMEOUT=30000 \
    SCREENSHOT_ON_FAIL=true

# Точка входа по умолчанию — smoke-тесты
ENTRYPOINT ["pytest"]
CMD ["-m", "smoke", "--html=reports/html/report.html", "--self-contained-html", "-v"]
