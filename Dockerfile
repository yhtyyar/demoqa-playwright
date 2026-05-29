FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

LABEL maintainer="yhtyyar"
LABEL description="DemoQA Playwright Automation Framework"

WORKDIR /app

# gosu — для безопасного переключения на tester в entrypoint
RUN apt-get update && apt-get install -y --no-install-recommends gosu \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей (кэшируется отдельным слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Создание пользователя tester (используется в entrypoint.sh)
RUN groupadd -r tester && useradd -r -g tester -d /home/tester -s /bin/bash tester \
    && mkdir -p /home/tester \
    && chown -R tester:tester /app /home/tester

# Создание директорий для отчётов (будут перезаписаны при volume mount,
# но нужны для запуска без volume)
RUN mkdir -p reports/html reports/xml reports/screenshots reports/allure reports/allure-results \
    && chmod -R 777 reports

# entrypoint: создаёт директории, фиксит права volume, запускает pytest от tester
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Переменные окружения по умолчанию
ENV BASE_URL=https://demoqa.com \
    BROWSER=chromium \
    BROWSER_CHANNEL="" \
    HEADLESS=true \
    TIMEOUT=30000 \
    SCREENSHOT_ON_FAIL=true

# entrypoint запускается от root, внутри переключается на tester через gosu
ENTRYPOINT ["/entrypoint.sh"]
CMD ["-m", "smoke", "--html=reports/html/report.html", "--self-contained-html", "-v"]
