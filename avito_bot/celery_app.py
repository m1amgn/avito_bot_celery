import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avito_bot.settings')

app = Celery('avito_bot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'get-access-token-every-3-hours': {
        'task': 'avito_autoreply_bot.tasks.get_access_token',
        'schedule': crontab(minute=0, hour='*/3')

    },
    'send-autoreply-every-3-minutes': {
        'task': 'avito_autoreply_bot.tasks.auto_reply',
        'schedule': crontab(minute='*/3')
    },
}
