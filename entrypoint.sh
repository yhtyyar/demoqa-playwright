#!/bin/bash
set -e

# Создать директории для отчётов (volume mount стирает те, что были при build)
mkdir -p /app/reports/html /app/reports/xml /app/reports/screenshots /app/reports/allure /app/reports/allure-results

# Открыть права для tester (volume mount приходит с правами root)
chown -R tester:tester /app/reports
chmod -R 777 /app/reports

# Запуск pytest от пользователя tester
exec gosu tester pytest "$@"
