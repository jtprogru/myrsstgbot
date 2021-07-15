from logging import getLogger

from celery import shared_task

from feeder.management.commands.rss_loader import RSSParser

logger = getLogger(__name__)


@shared_task
def task_rss_loader():
    logger.info("[*] Run task - task_rss_loader")
    rssparser = RSSParser()
    rssparser.parse_all()
    logger.info("[*] Stop task - task_rss_loader")
