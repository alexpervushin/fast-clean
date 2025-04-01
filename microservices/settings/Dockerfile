FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

COPY microservices/settings/pyproject.toml microservices/settings/uv.lock /app/

COPY microservices/shared /app/microservices/shared
COPY microservices/settings /app/microservices/settings

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev


ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["python", "-m", "microservices.settings.entrypoints.web_server"]