from project.queue.celery import celery_app


@celery_app.task(acks_late=True)
def test_celery(value: str) -> str:
    print(f"{value}")
    return f"{value}"
