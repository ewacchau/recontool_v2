.DEFAULT_GOAL := help

venv/bin/activate: requirements.txt
	python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt

docker-up: ## Build and start all containers
	docker-compose up --build

docker-down: ## Stop containers
	docker-compose down

migrate: ## Apply database migrations
	docker-compose exec web flask db upgrade

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' Makefile | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
