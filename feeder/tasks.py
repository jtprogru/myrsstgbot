from logging import getLogger

from django.conf import settings

from celery import shared_task

from feeder.management.commands.rss_loader import RSSParser
from feeder.management.commands.load_source import Loader

logger = getLogger(__name__)


def task_logger(f):
    """Простейший декоратор-логгер"""
    logger.info(f"[*] Run task – {f}")
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            logger.error(error_message)
            raise e
    logger.info(f"[*] Stop task - {f}")
    return inner


@task_logger
@shared_task
def task_rss_loader():
    rssparser = RSSParser()
    res = rssparser.parse_all()
    return res


@task_logger
@shared_task
def task_source_loader():
    loader = Loader(src_file=settings.FEEDER_DEFAULT_SRC_FILE)
    loader.load()

