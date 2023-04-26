from __future__ import absolute_import

from celery import Celery

from project.settings import settings

celery_app = Celery(
    "project",
    backend=str(settings.redis_url),
    broker=str(settings.rabbit_url),
)

celery_app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == "__main__":
    celery_app.start()
