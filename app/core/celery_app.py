from app.core.config import settings
from celery import Celery

CELERY_BROKER_URL = f"{settings.REDIS_URL}/0"
CELERY_RESULT_BACKEND = f"{settings.REDIS_URL}/1"

celery_app = Celery(
    "image_processor",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['app.tasks.image_tasks']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    result_expires=3600,
)
