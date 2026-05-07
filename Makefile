.PHONY: initial test format lint up down

# Environment detection and default values
PYTHON ?= python3
PIP ?= pip3
DOCKER_COMPOSE ?= docker-compose
ifneq (, $(shell command -v docker compose 2> /dev/null))
    DOCKER_COMPOSE = docker compose
endif

initial:
	@echo "Initializing Schedule Module..."
	@echo "1. Checking environment..."
	@$(PYTHON) -m venv .venv || true
	@.venv/bin/python -m pip install --upgrade pip
	@.venv/bin/pip install -e .[dev]
	@echo "2. Starting Infrastructure (PostgreSQL)..."
	@$(DOCKER_COMPOSE) -f infra/docker-compose.yml up -d
	@echo "3. Waiting for PostgreSQL to be ready..."
	@sleep 5
	@echo "4. Running Bootstrap and Migrations..."
	@.venv/bin/python -m src.cli bootstrap
	@echo "Initialization complete!"

up:
	@$(DOCKER_COMPOSE) -f infra/docker-compose.yml up -d

down:
	@$(DOCKER_COMPOSE) -f infra/docker-compose.yml down

test:
	@.venv/bin/pytest tests/
