from .constants import STATUS_NEW
from .management.commands.rss_loader import RSSParser
from .models import Task


def task_parse_all(**kwargs):
    tasks = Task.objects.filter(status=STATUS_NEW).all()
    pars = RSSParser()
    if len(tasks) > 0:
        pars.parse_all()
