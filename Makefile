.PHONY: lint-check run clean

lint-check:
	@echo "Running flake8..."
	uv run flake8 app
	@echo "Running mypy..."
	uv run mypy app

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

clean:
	rm -rf static/*.csv
	rm -rf .mypy_cache
	rm -rf .pytest_cache