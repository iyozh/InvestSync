from celery import Celery
from app.src.core.config import settings

app = Celery('invest-sync', broker=settings.CELERY_BROKER_URL)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'app.src.tasks.celery_app.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
}

@app.task
def add(x, y):
    z = x + y
    print(z)
