.PHONY: install test test-api test-ui test-db test-allure docker-up docker-down

install:
	pip install -r requirements.txt

test:
	pytest -v

test-api:
	pytest api_tests/ -v -m api

test-ui:
	pytest ui_tests/ -v -m ui

test-db:
	pytest db_tests/ -v -m db

test-allure:
	pytest --alluredir=reports/allure-results

docker-up:
	docker-compose up --build

docker-down:
	docker-compose down
