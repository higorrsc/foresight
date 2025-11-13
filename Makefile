# Makefile para o projeto ForeSight
# Ajuda a automatizar tarefas comuns de desenvolvimento e verificação de qualidade.

# Define o interpretador a ser usado. O .PHONY garante que os comandos sejam sempre executados.
.PHONY: help install run check format lint type-check test

# --- Comandos Principais ---

help:
	@echo "Comandos disponíveis:"
	@echo "  make install      - Instala/sincroniza as dependências do projeto com uv."
	@echo "  make run          - Inicia o servidor da API em modo de desenvolvimento."
	@echo "  make check        - Executa todas as verificações de qualidade (lint, type-check, test)."
	@echo "  make format       - Formata todo o código com black."
	@echo "  make lint         - Verifica a formatação do código com black."
	@echo "  make type-check   - Executa a verificação de tipos com mypy."
	@echo "  make test         - Executa a suíte de testes completa com pytest."

install:
	@echo "📦 Instalando dependências..."
	@uv sync

run:
	@echo "🚀 Iniciando a API em http://127.0.0.1:8000..."
	@uv run uvicorn src.api.main:app --reload

check: lint type-check test
	@echo "✅ Todas as verificações passaram com sucesso!"

format:
	@echo "🎨 Formatando o código com ruff..."
	@uv run ruff format .
	@uv run ruff check --fix .

secret:
	@echo "📦 Gerando secrets para o projeto..."
	@python -c "import secrets;print(secrets.token_hex(32))"

# --- Comandos de Verificação de Qualidade ---

lint:
	@echo "🔍 Verificando a formatação do código com ruff..."
	@uv run ruff check .
	@uv run ruff format --check .

type-check:
	@echo " typing: Verificando os tipos com mypy..."
	@uv run mypy .

test:
	@echo "🧪 Executando os testes com pytest..."
	@uv run pytest

coverage:
	@echo "🧪 Gerando relatório de cobertura de testes..."
	@uv run pytest --cov=src --cov-report=term-missing --cov-report=html
