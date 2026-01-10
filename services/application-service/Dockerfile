FROM python:3.12-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency metadata
COPY pyproject.toml uv.lock* ./

# Install deps (no-op if empty)
RUN uv sync --frozen || true

# Copy app code
COPY app ./app

# Run service
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]