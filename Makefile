.PHONY: format lint type-check check clean

format:
	black .

lint:
	flake8 .

check: format lint

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +

help:
	@echo "Available commands:"
	@echo "  make format      - Format code using black"
	@echo "  make lint        - Run flake8 linter"
	@echo "  make check       - Run all checks (format, lint, type-check)"
	@echo "  make clean       - Remove cache directories"