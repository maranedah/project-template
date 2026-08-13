# Canonical commands — the only place commands are defined. Docs link here, never restate.
.DEFAULT_GOAL := help
SHELL := /bin/bash

-include .env
export
APP_BACKEND_PORT ?= 8100
APP_FRONTEND_PORT ?= 3100
APP_DB_PORT ?= 5532

VENV := backend/.venv

help: ## List targets
	@grep -hE '^[a-zA-Z_-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "%-10s %s\n", $$1, $$2}'

$(VENV): backend/requirements.txt backend/requirements-dev.txt frontend/e2e/requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -q -r backend/requirements.txt -r backend/requirements-dev.txt -r frontend/e2e/requirements.txt
	$(VENV)/bin/pip install -q --no-deps -e backend
	touch $(VENV)

venv: $(VENV) ## Create backend virtualenv (also used by e2e)

test: $(VENV) ## Backend unit tests, parallel (unittest classes via pytest-xdist)
	cd backend && .venv/bin/pytest -n auto

lint: $(VENV) ## ruff + hexagonal import contracts + docs tree lint
	cd backend && .venv/bin/ruff check app tests && .venv/bin/lint-imports
	$(VENV)/bin/python docs/lint_docs.py

build: ## Build all docker images (layer-cached; second run is near-instant)
	docker compose build

up: ## Start the full stack (db → migrate → backend → frontend)
	docker compose up -d

down: ## Stop the stack
	docker compose down

logs-errors: ## Tail the per-service error logs (timestamped, errors only)
	tail -n 50 backend/var/log/*-errors.log

e2e: $(VENV) ## Selenium UI suite, parallel (stack must be up)
	cd frontend/e2e && $(CURDIR)/$(VENV)/bin/pytest -n auto

verify: lint test build ## Full check: lint, tests, images, live stack, API, e2e
	docker compose up -d
	@echo "waiting for backend on :$(APP_BACKEND_PORT)..."
	@for i in $$(seq 1 45); do curl -fsS localhost:$(APP_BACKEND_PORT)/health >/dev/null 2>&1 && break; sleep 2; done
	curl -fsS localhost:$(APP_BACKEND_PORT)/health
	curl -fsS -X POST localhost:$(APP_BACKEND_PORT)/api/items -H 'Content-Type: application/json' \
		-d '{"name":"verify","source":"make-verify"}' >/dev/null
	curl -fsS localhost:$(APP_BACKEND_PORT)/api/items | grep -q '"verify"'
	curl -fsS localhost:$(APP_FRONTEND_PORT)/ >/dev/null
	$(MAKE) e2e
	@echo "── verify OK ──"

.PHONY: help venv test lint build up down logs-errors e2e verify
