from logging import getLogger

from celery import shared_task

from django.core.management import call_command
# from feeder.management.commands.rss_loader import RSSParser

logger = getLogger(__name__)


@shared_task(name="task_rss_loader")
def task_rss_loader():
    logger.info("[*] Run task - task_rss_loader")
    # rssparser = RSSParser()
    # rssparser.parse_all()
    call_command("rss_loader", )
    logger.info("[*] Stop task - task_rss_loader")
