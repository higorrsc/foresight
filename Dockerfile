# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.6
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    UV_PROJECT_ENVIRONMENT=/usr/local \
    UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create non-root user
ARG UID=10001

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --frozen

# Copy app
COPY src ./src
COPY alembic.ini .
COPY alembic ./alembic

# Permissions
RUN chown -R appuser:appuser /app
RUN mkdir -p /tmp/uv-cache && chown -R appuser:appuser /tmp/uv-cache

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && uvicorn src.api.main:app --host 0.0.0.0 --port 8000"]
