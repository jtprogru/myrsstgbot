from datetime import datetime
from logging import getLogger
from typing import List

import requests
from django.core.management import BaseCommand, CommandError
from django.conf import settings

import feedparser
from feedparser import FeedParserDict

from feeder.constants import STATUS_READY, STATUS_RUNNING, STATUS_NEW
from feeder.models import Task, RSSItem

logger = getLogger(__name__)


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            raise e

    return inner


class RSSParser:
    PAGE_LIMIT = 10

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
            'Accept-Language': 'ru',
        }
        self.task = None

    @log_errors
    def get_rss_feed(self, url: str) -> FeedParserDict:
        self.task.status = STATUS_RUNNING
        return feedparser.parse(url)

    def find_task(self):
        obj = Task.objects.filter(status=STATUS_NEW).first()
        if not obj:
            raise CommandError('no tasks found')
        self.task = obj
        logger.info(f'Работаем над заданием {self.task.title}')

    def running_task(self):
        self.task.status = STATUS_RUNNING
        self.task.save()
        logger.info(f'Работаем над заданием заданием {self.task.title}')

    def finish_task(self):
        self.task.status = STATUS_READY
        self.task.save()
        logger.info(f'Завершили задание {self.task.title}')

    def get_rss_item_list(self, feed: FeedParserDict) -> List[RSSItem]:
        rss_item = []
        for item in feed['entries']:
            try:
                dtt = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %Z')
                logger.debug(f"Дата публикации: {item['published']}")
            except:
                dtt = datetime.strptime(item['published'], '%a, %d %b %Y %H:%M:%S %z')
                logger.debug(f"Дата публикации: {item['published']}")

            obj = RSSItem(
                title=item['title'],
                link=item['link'],
                pub_date=dtt,
                description=item['summary']
            )
            obj.save()
            rss_item.append(obj)

        return rss_item

    def parse_all(self):
        # Выбрать какое-нибудь задание
        self.find_task()

        feed = self.get_rss_feed(self.task.url)
        logger.info(f'Всего постов в RSS-ленте: {len(feed["entries"])}')

        self.get_rss_item_list(feed)

        # Завершить задание
        self.finish_task()


class Command(BaseCommand):
    help = 'Парсинг RSS'

    def handle(self, *args, **options):
        rssparser = RSSParser()
        rssparser.parse_all()
        # print(f"Последняя запись:\n{feed['entries'][0]['title']}\n{feed['entries'][0]['link']}")
