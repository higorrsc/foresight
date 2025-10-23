# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files and keeps stdio unbuffered.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Explicitly set PYTHONPATH for imports starting with 'src'
    PYTHONPATH=/app/src \
    UV_CACHE_DIR=/app/.uv_cache

WORKDIR /app

# Create a non-privileged user
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Install uv globally
RUN python -m pip install uv
RUN mkdir -p ${UV_CACHE_DIR} && chown appuser:appuser ${UV_CACHE_DIR}

# Copy only dependency definition files first to leverage Docker cache
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install production dependencies using uv
# --no-dev excludes development dependencies like pytest, black, mypy
RUN uv sync --no-dev

# Copy the rest of the application code needed for runtime
COPY --chown=appuser:appuser src ./src
COPY --chown=appuser:appuser main.py ./main.py
COPY --chown=appuser:appuser alembic.ini ./alembic.ini
COPY --chown=appuser:appuser alembic ./alembic

# Change ownership of the entire app directory (just in case)
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user *before* running the application
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
# 1. Apply Alembic migrations
# 2. Start Uvicorn server
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000"]
