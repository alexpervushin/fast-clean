from celery import Celery
from celery.schedules import crontab

from microservices.scheduler.infrastructure.config import get_settings
from microservices.shared.infrastructure.observability.sentry import setup_sentry

settings = get_settings()

if settings.sentry and settings.sentry.dsn:
    setup_sentry(settings)

celery_app = Celery(
    "devwatch_tasks",
    broker=settings.celery.broker.url,
    backend=settings.celery.result_backend.url,
    include=[
        "microservices.scheduler.entrypoints.celery_beat"
    ],
)

celery_app.conf.update(
    timezone=settings.celery.timezone,
)

@celery_app.task(name="trigger_all_collectors")
def trigger_all_collectors_placeholder(*args, **kwargs):
    pass

celery_app.conf.beat_schedule = {
    "collect-every-5-minutes": {
        "task": "trigger_all_collectors",
        "schedule": crontab(minute="*/5"),
    },
}

