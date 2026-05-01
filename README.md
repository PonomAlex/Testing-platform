# E2E Testing Platform

Pet-проект для автоматизации тестирования интернет-магазина на трех уровнях:

- API тесты (`requests` + `jsonschema`)
- UI тесты (`selenium` + Page Object Model)
- DB тесты (`psycopg2` + PostgreSQL)

## Стек

- Python 3.10+
- Pytest
- Requests + JSON Schema
- Selenium WebDriver
- PostgreSQL + psycopg2
- Allure Reports
- Docker + Docker Compose
- GitHub Actions

## Структура

```text
e2e-testing-platform/
├── api_tests/
├── ui_tests/
│   └── pages/
├── db_tests/
├── common/
├── data/
├── reports/
├── .github/workflows/test.yml
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── pytest.ini
```

## Быстрый старт

1. Установи зависимости:

```bash
pip install -r requirements.txt
```

2. Скопируй переменные окружения:

```bash
cp .env.example .env
```

3. Подними БД (если локально):

```bash
docker-compose up -d postgres
```

4. Инициализируй схему:

```bash
psql -h localhost -U testuser -d testdb -f data/init.sql
```

## Запуск тестов

```bash
# API
pytest api_tests/ -v -m api

# UI
pytest ui_tests/ -v -m ui

# DB
pytest db_tests/ -v -m db

# Все
pytest -v
```

## Отчеты Allure

```bash
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## Запуск в Docker

```bash
docker-compose up --build
docker-compose down
```

## Что покрыто

- CRUD + фильтрация + комментарии + схемы + негативные кейсы для JSONPlaceholder
- Логин, негативный логин, корзина, подсчет товаров, полный checkout flow для SauceDemo
- Проверка таблиц, FK, уникальности email, согласованности цен и транзакций в PostgreSQL