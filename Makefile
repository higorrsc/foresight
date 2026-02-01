# Makefile for the ForeSight project
# Helps automate common development and quality-check tasks.

.PHONY: help install run check format lint type-check test coverage secret

# --- Main Commands ---

help:
	@echo "Available commands:"
	@echo "  make install      - Install/sync project dependencies using uv."
	@echo "  make run          - Start the API server in development mode."
	@echo "  make check        - Run all quality checks (lint, type-check, test)."
	@echo "  make format       - Format the entire codebase with ruff."
	@echo "  make lint         - Run lint checks with ruff."
	@echo "  make type-check   - Run static type checks with mypy."
	@echo "  make test         - Run the full test suite with pytest."
	@echo "  make coverage     - Generate test coverage reports."
	@echo "  make secret       - Generate a random project secret."

install:
	@echo "📦 Installing dependencies..."
	@uv sync

run:
	@echo "🚀 Starting API at http://127.0.0.1:8000..."
	@uv run uvicorn src.api.main:app --reload

check: lint type-check test
	@echo "✅ All quality checks passed successfully!"

format:
	@echo "🎨 Formatting code with ruff..."
	@uv run ruff format .
	@uv run ruff check --fix .

secret:
	@echo "🔐 Generating project secret..."
	@python -c "import secrets; print(secrets.token_hex(32))"

# --- Quality Assurance Commands ---

lint:
	@echo "🔍 Running lint checks with ruff..."
	@uv run ruff check .
	@uv run ruff format --check .

type-check:
	@echo "🧠 Running type checks with mypy..."
	@uv run mypy .

test:
	@echo "🧪 Running tests with pytest..."
	@uv run pytest

coverage:
	@echo "📊 Generating test coverage report..."
	@uv run pytest --cov=src --cov-report=term-missing --cov-report=html
