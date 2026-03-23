FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

LABEL maintainer="yhtyyar"
LABEL description="DemoQA Playwright Automation Framework"

WORKDIR /app

# Установка зависимостей (кэшируется отдельным слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание директорий для отчётов
RUN mkdir -p reports/html reports/xml reports/screenshots reports/allure

# Пользователь без root-прав (безопасность)
RUN useradd --create-home --shell /bin/bash tester \
    && chown -R tester:tester /app
USER tester

# Точка входа по умолчанию — smoke-тесты
ENTRYPOINT ["pytest"]
CMD ["-m", "smoke", "--html=reports/html/report.html", "--self-contained-html", "-v"]
