.PHONY: install test lint format pre-commit-install pre-commit-run

install:
	python -m pip install -r requirements.txt -r requirements-dev.txt

test:
	python -m pytest -q

lint:
	ruff check .

format:
	ruff format .

pre-commit-install:
	python -m pip install pre-commit
	pre-commit install

pre-commit-run:
	pre-commit run --all-files
