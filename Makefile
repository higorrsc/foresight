# Virtual environment directory (default: .venv)
VENV_DIR ?= .venv

# UV wrapper commands
UV = @uv
RUN_PY = $(UV) run python
RUN_TOOL = $(UV) run

# Detect Operating System for manual paths (fallback)
ifdef ComSpec
	PYTHON_EXEC = $(VENV_DIR)/Scripts/python.exe
else
	PYTHON_EXEC = $(VENV_DIR)/bin/python
endif

.PHONY: help venv install install-prd export-req run check format lint type-check test coverage secret check-python

# === Server ===

run-uvicorn: check-python
	@echo "Starting API server at http://127.0.0.1:8000 with Uvicorn..."
	$(RUN_TOOL) uvicorn src.api.main:app --reload

run-fastapi: check-python
	@echo "Starting API server at http://127.0.0.1:8000 with FastAPI..."
	$(RUN_TOOL) uv run fastapi dev -e src.api.main:app


# === Environment Setup ===

# Create virtual environment
venv:
	@echo "Creating virtual environment in $(VENV_DIR)..."
	$(UV) venv $(VENV_DIR)

# Install dependencies from pyproject.toml (including dev)
install:
	@echo "Installing project dependencies (including dev)..."
	$(UV) sync

# Install dependencies without dev packages
install-prd:
	@echo "Installing project dependencies (production only)..."
	$(UV) sync --no-dev

# Install dependencies from requirements.txt (pip fallback)
install-pip: check-python
	@echo "Installing project dependencies from requirements.txt using pip..."
	$(PYTHON_EXEC) -m pip install --upgrade pip
	$(PYTHON_EXEC) -m pip install -r requirements.txt

# Export dependencies to requirements.txt
export-req:
	@echo "Exporting dependencies to requirements.txt..."
	$(UV) export --no-dev --no-hashes --no-annotate --output-file requirements.txt --format requirements.txt

# Verify if python executable exists in venv
check-python:
	@if [ ! -f "$(PYTHON_EXEC)" ]; then \
		echo "Virtual environment not found at $(PYTHON_EXEC)"; \
		echo "Run 'make venv' to create the virtual environment."; \
		exit 1; \
	fi

# === Quality & Testing ===

check: lint type-check test
	@echo "All quality checks passed successfully."

# Format (Ruff)
format: check-python
	@echo "Formatting codebase with Ruff..."
	$(RUN_TOOL) ruff format .
	$(RUN_TOOL) ruff check . --fix

# Lint and Format Check (Ruff)
lint: check-python
	@echo "Running lint checks with Ruff..."
	$(RUN_TOOL) ruff check .
	$(RUN_TOOL) ruff format --check .

# Type Checking (Mypy)
type-check: check-python
	@echo "Running static type checking with MyPy..."
	$(RUN_TOOL) mypy .

# Tests (PyTest)
test: check-python
	@echo "Running test suite with PyTest..."
	$(RUN_TOOL) pytest -q

coverage: check-python
	@echo "Generating test coverage report..."
	$(RUN_TOOL) pytest --cov=src --cov-report=term-missing --cov-report=html

# === Utilities ===

secret: check-python
	@echo "Generating project secret..."
	$(RUN_PY) -c "import secrets; print(secrets.token_hex(32))"

# === Help ===

help:
	@echo "Available commands:"
	@echo ""
	@echo "Server:"
	@echo "  make run                - Start the API server in development mode"
	@echo ""
	@echo "Quality & Testing:"
	@echo "  make check              - Run lint, type-check and tests"
	@echo "  make format             - Auto-format and fix code (Ruff)"
	@echo "  make lint               - Check code style (Ruff)"
	@echo "  make type-check         - Run static type checking (MyPy)"
	@echo "  make test               - Run tests"
	@echo "  make coverage           - Run tests with coverage report"
	@echo ""
	@echo "Environment:"
	@echo "  make venv               - Create virtual environment in $(VENV_DIR)"
	@echo "  make install            - Install dependencies (including dev)"
	@echo "  make install-prd        - Install dependencies without dev packages"
	@echo "  make export-req         - Export dependencies to requirements.txt"
	@echo ""
	@echo "Utilities:"
	@echo "  make secret             - Generate a random project secret"
	@echo ""
	@echo "Use VENV_DIR=<path> to override the virtual environment directory (default: .venv)"
