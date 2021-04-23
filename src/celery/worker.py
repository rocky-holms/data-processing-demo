import os

from celery import Celery

CELERY_BROKER_URL = os.getenv("REDISSERVER", "redis://redis_server:6379")
CELERY_RESULT_BACKEND = os.getenv("REDISSERVER", "redis://redis_server:6379")

celery_conn = Celery(
    "celery",
    backend=CELERY_BROKER_URL,
    broker=CELERY_RESULT_BACKEND,
)
celery_conn.conf.task_serializer = "pickle"
celery_conn.conf.result_serializer = "pickle"
celery_conn.conf.accept_content = ["pickle"]
