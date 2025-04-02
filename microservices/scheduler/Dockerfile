FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

COPY microservices/scheduler/pyproject.toml microservices/scheduler/uv.lock /app/

COPY microservices/shared /app/microservices/shared
COPY microservices/scheduler /app/microservices/scheduler

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"

CMD ["celery", "-A", "microservices.scheduler.entrypoints.celery_beat.celery_app", "beat", "--loglevel=info", "--pidfile=/tmp/celerybeat.pid"]