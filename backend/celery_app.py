import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

broker_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
result_backend = broker_url

celery_app = Celery(
    "answerflow",
    broker=broker_url,
    backend=result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_always_eager=False,
    result_expires=3600,
)
