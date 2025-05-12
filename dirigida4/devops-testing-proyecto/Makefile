.PHONY: test ci coverage format lint type clean mutation report

# Variables
PYTHON = python
PYTEST = pytest
PYTEST_ARGS = -v
COVERAGE = pytest --cov=src --cov-report=term --cov-report=html
TOX = tox
BLACK = black
MYPY = mypy
MUTATION = ./run_mutation.sh
REPORT = pytest --md-report

# Targets
test:
	$(PYTEST) $(PYTEST_ARGS)

coverage:
	$(COVERAGE)

format:
	$(BLACK) src tests

lint:
	$(TOX) -e lint

type:
	$(TOX) -e type

mutation:
	$(MUTATION)

report:
	$(REPORT)

ci:
	$(TOX)
	$(REPORT)

clean:
	rm -rf .tox
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf .pytest_cache
	rm -rf **/__pycache__
	rm -rf **/*.pyc
	rm -rf **/*.pyo
	rm -rf **/*.pyd
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf .mutmut-cache
	rm -rf reports/latest.md

help:
	@echo "Available targets:"
	@echo "  test       Run tests with pytest"
	@echo "  coverage   Run tests with coverage report"
	@echo "  format     Format code with black"
	@echo "  lint       Run linting checks"
	@echo "  type       Run type checking"
	@echo "  mutation   Run mutation tests on services.py"
	@echo "  report     Generate test report in Markdown"
	@echo "  ci         Run all CI checks with tox"
	@echo "  clean      Clean all build and test artifacts"
	@echo "  help       Show this help message" 