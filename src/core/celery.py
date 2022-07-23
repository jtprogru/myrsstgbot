import os

from django.conf import settings

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object.
app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'task_rss_loader': {
        'task': 'feeder.tasks.task_rss_loader',
        'schedule': 60 * 5,
    },
    'task_source_loader': {
        'task': 'feeder.tasks.task_source_loader',
        'schedule': 60 * 10,
    }
}
