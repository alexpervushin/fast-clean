FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

COPY microservices/users/pyproject.toml microservices/users/uv.lock /app/

COPY microservices/shared /app/microservices/shared
COPY microservices/users /app/microservices/users

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["python", "-m", "microservices.users.entrypoints.web_server"]