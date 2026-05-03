from celery import Celery

from setup.config import Settings, settings


def create_celery_app(app_settings: Settings = settings) -> Celery:
    broker_url = app_settings.celery.broker_url or app_settings.redis.url
    result_backend = app_settings.celery.result_backend or app_settings.redis.url

    celery_app = Celery(
        "citadel",
        broker=broker_url,
        backend=result_backend,
    )
    celery_app.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        imports=("notification_worker",),
    )
    return celery_app


celery_app = create_celery_app()
