import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website.settings')

app = Celery('website')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


# добавляем задачу, которая будет выполняться в фоне с заданной периодичностью
# на самом деле в заданный момент времени она будет передаваться воркеру (worker)
# для выполнения
# app.conf.beat_schedule = {
#     'send-email-every-5-minutes': {             # имя task
#         'task': 'main.tasks.send_beat_email',   # что запускаем
#         'schedule': crontab(minute='*/5')       # интервал (есть разные варианты, см доку)
#     }
# }
