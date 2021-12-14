.PHONY: help test black list isort clean install_pyenv install_poetry setup_env

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

help: ## this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

test: ## run test and show coverage
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS)

black: ## format all code
	$(CMD) black .

lint: ## run the static type checker and the linter
	$(CMD) flake8 $(PYMODULE) $(TESTS) $(EXTRACODE) && \
	$(CMD) mypy $(PYMODULE) $(TESTS) $(EXTRACODE)

isort: ## sort all imports
	$(CMD) isort $(PYMODULE) $(TESTS) $(EXTRACODE)

clean: # delete all files in .gitignore
	git clean -Xdf

# Virtual env
# -----------------------------------------------------------------------------

install_pyenv: ## install yenv
	curl https://pyenv.run | bash

install_poetry: ## install poetry
	curl -sSL https://install.python-poetry.org | python3 -

setup_env: ## setup the virtual env
	pyenv install $(PYTHON_VERSION)
	pyenv local $(PYTHON_VERSION)
	poetry env use $(PYTHON_VERSION)
	poetry install




