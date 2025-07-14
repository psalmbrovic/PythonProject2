.PHONY: install test test-smoke test-regression clean report

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

test-smoke:
	pytest tests/ -m smoke -v

test-regression:
	pytest tests/ -m regression -v

test-parallel:
	pytest tests/ -n auto -v

test-headless:
	HEADLESS=true pytest tests/ -v

clean:
	rm -rf reports/
	rm -rf screenshots/
	rm -rf logs/
	rm -rf .pytest_cache/
	rm -rf __pycache__/
	find . -name "*.pyc" -delete

report:
	allure serve reports/allure-results

generate-allure:
	allure generate reports/allure-results -o reports/allure-report --clean

setup-dirs:
	mkdir -p reports screenshots logs test_data

help:
	@echo "Available commands:"
	@echo "  install       - Install dependencies"
	@echo "  test          - Run all tests"
	@echo "  test-smoke    - Run smoke tests"
	@echo "  test-regression - Run regression tests"
	@echo "  test-parallel - Run tests in parallel"
	@echo "  test-headless - Run tests in headless mode"
	@echo "  clean         - Clean generated files"
	@echo "  report        - Serve Allure report"
	@echo "  generate-allure - Generate Allure report"
	@echo "  setup-dirs    - Create required directories"