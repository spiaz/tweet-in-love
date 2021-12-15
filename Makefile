
# Variables definitions
# -----------------------------------------------------------------------------

CMD:=poetry run
PYMODULE:=tweet_in_love
TESTS:=tests
EXTRACODE:=app

SHELL:=/bin/bash
PYTHON_VERSION:=3.9.5

# Dev stuff
# -----------------------------------------------------------------------------
.PHONY: help test black list isort clean generate_dot_env

help: ## this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## run test and show coverage
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

black: ## format all code
	$(CMD) black .

lint: ## run the static type checker and the linter
	$(CMD) flake8 $(PYMODULE) $(TESTS) $(EXTRACODE)
	$(CMD) mypy $(PYMODULE) $(TESTS) $(EXTRACODE)

isort: ## sort all imports
	$(CMD) isort $(PYMODULE) $(TESTS) $(EXTRACODE)

clean: ## delete all files in .gitignore
	git clean -Xdf

generate_dot_env: ## Cenerate an example .env file
	@if [[ ! -e .env ]]; then \
		cp .env.example .env; \
	fi

# Virtual env
# -----------------------------------------------------------------------------
.PHONY: install_poetry install install_dev

install_poetry: ## install virtual env
	pip install poetry

install: ## install requirements
	poetry env use $(PYTHON_VERSION)
	poetry install --no-dev

install_dev: ## install dev requirements
	install
	poetry install

# Deploy
# -----------------------------------------------------------------------------
.PHONY: docker_build docker_deploy docker_down up

docker_build: ## create docker volume
	docker build -t tweet_in_love .

docker_up: generate_dot_env ## run docker volume
	docker run -p 8080:8080 tweet_in_love

docker_down: ## stop docker volume
	docker stop tweet_in_love

up: ## launch the app locally
	$(CMD) python -m main

