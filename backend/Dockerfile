FROM ghcr.io/astral-sh/uv:0.9.5 AS uv
FROM python:3.13-slim AS builder

COPY --from=uv /uv /usr/local/bin/uv
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --frozen --no-dev --extra hopsworks --no-editable

FROM python:3.13-slim
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    KEDRO_DISABLE_TELEMETRY=1 \
    DO_NOT_TRACK=1
RUN useradd --create-home --uid 10001 app
WORKDIR /app
COPY --from=builder --chown=app:app /app /app
COPY --chown=app:app config/base ./config/base
RUN mkdir -p config/local data/raw data/processed data/predictions models \
    && chown -R app:app /app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=3)"
CMD ["uvicorn", "supply_chain.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
