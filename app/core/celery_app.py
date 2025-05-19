from celery import Celery
from .config import settings

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_soft_time_limit=600,  
    task_time_limit=900, 
    task_routes={
        'app.tasks.*': {'queue': 'embedding_queue'}
    }
) 