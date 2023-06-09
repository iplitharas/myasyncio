# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

#########################################################################################
####################### Local  Setup ####################################################

create-env: ## Create python virtual env
	python -m venv .env && source .env/bin/activate && pip install --upgrade pip

poetry-env: create-env ## Create and install environment for local dev
	  source .env/bin/activate && poetry install

install-hooks: ## Install hooks
	pre-commit install

install-local:poetry-env install-hooks


check: ## Run isort black and pylint in all files
	isort .
	black .

.PHONY: help create-env install-local install-hooks check

help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)