import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myrsstgbot.settings")
app = Celery("myrsstgbot")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
