.PHONY: lint style black black-check isort isort-check flake8 tests install-dev install docs

black:
	black scenario_player_services

isort:
	isort --recursive scenario_player_services

isort-check:
	isort --recursive --diff --check-only scenario_player_services

black-check:
	black --check --diff scenario_player_services

flake8:
	flake8 scenario_player_services --max-doc-length=120 --max-line-length=100

style: isort black

lint: flake8 black-check isort-check

install:
	pip install .

install-dev:
	pip install ".[dev]" ".[docs]"

tests:
	pytest --cov=scenario_player_services

docs:
	cd docs/ && make html
