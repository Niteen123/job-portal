FROM python:3.12-slim

WORKDIR /app

# Install uv (pinned version for faster builds)
COPY --from=ghcr.io/astral-sh/uv:0.4.11 /uv /usr/local/bin/uv

# Copy dependency metadata
COPY pyproject.toml uv.lock* ./

# Install deps
RUN uv sync --frozen || true

# Copy app code
COPY app ./app

# Run service
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
