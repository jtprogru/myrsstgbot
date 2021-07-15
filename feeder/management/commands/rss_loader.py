from datetime import datetime
from django.utils import timezone
from logging import getLogger
from typing import List

from django.core.management import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule

import feedparser
from feedparser import FeedParserDict

from feeder.constants import STATUS_READY, STATUS_RUNNING, STATUS_NEW
from feeder.models import Source, RSSItem

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
    def __init__(self):
        self.source = None

    @log_errors
    def get_rss_feed(self, url: str) -> FeedParserDict:
        self.source.status = STATUS_RUNNING
        return feedparser.parse(url)

    def find_source(self):
        obj = Source.objects.filter(status=STATUS_NEW).first()
        if not obj:
            raise CommandError('no sources found')
        self.source = obj
        logger.info(f'Работаем над заданием {self.source.title}')

    def running_source(self):
        self.source.status = STATUS_RUNNING
        self.source.save()
        logger.info(f'Работаем над заданием {self.source.title}')

    def finish_source(self):
        self.source.status = STATUS_READY
        self.source.save()
        logger.info(f'Завершили задание {self.source.title}')

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
        self.find_source()

        feed = self.get_rss_feed(self.source.url)
        logger.info(f'Всего постов в RSS-ленте: {len(feed["entries"])}')

        self.get_rss_item_list(feed)

        # Завершить задание
        self.finish_source()


class Command(BaseCommand):
    help = 'Парсинг RSS'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        rssparser = RSSParser()
        status = STATUS_NEW
        source = Source.objects.get(pk=options['url'])
        if status == 0:
            PeriodicTask.objects.create(
                name='task_rss_loader',
                task='task_rss_loader',
                interval=IntervalSchedule.objects.get(every=120, period='seconds'),
                start_time=timezone.now(),
            )
        else:
            source.status = STATUS_READY
            source.refresh_from_db()
            logger.info('[*] Source {} status -> {}'.format(source.id, source.status))

        rssparser.parse_all()
