from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')

app = Celery('banking_system')


app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'calculate_interest': {
        'task': 'calculate_interest',
        # http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html
        'schedule': crontab(0, 0, day_of_month='1'),
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
