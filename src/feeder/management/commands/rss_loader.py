from datetime import datetime
from django.utils import timezone
from logging import getLogger
from typing import List

from django.core.management import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule

import dateparser
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


@log_errors
def datetime_parse(date_string: str) -> datetime:
    return dateparser.parse(date_string)


class RSSParser:
    """
    Класс парсера для RSS-фида
    """
    def __init__(self):
        self.source = None

    @log_errors
    def get_rss_feed(self, url: str) -> FeedParserDict:
        """
        Получаем dict из RSS-фида
        """
        self.source.status = STATUS_RUNNING
        return feedparser.parse(url)

    def find_source(self):
        """
        Ищем источник в статесу "Новый"
        """
        obj = Source.objects.filter(status=STATUS_NEW).first()
        if not obj:
            raise CommandError('no sources found')
        self.source = obj
        # logger.info(f'Работаем над заданием {self.source.title}')

    def running_source(self):
        self.source.status = STATUS_RUNNING
        self.source.save()
        logger.info(f'Работаем над заданием {self.source.title}')

    def finish_source(self):
        self.source.status = STATUS_READY
        self.source.save()
        logger.info(f'Завершили задание {self.source.title}')

    @log_errors
    def check_rssitem_exists(self, url: str):
        return RSSItem.objects.filter(link=url).first()

    @log_errors
    def get_rss_item_list(self, feed: FeedParserDict) -> List[RSSItem]:
        rss_item = []
        for item in feed['entries']:
            dtt = datetime_parse(item['published'])

            obj_count = self.check_rssitem_exists(item['link'])

            if obj_count == 0:
                obj = RSSItem.objects.create(
                    title=item['title'],
                    link=item['link'],
                    pub_date=dtt,
                    description=item['summary']
                )
                rss_item.append(obj)

        return rss_item

    def parse_all(self):
        # Выбрать какое-нибудь задание
        self.find_source()

        feed = self.get_rss_feed(self.source.url)
        logger.info(f'Всего постов в RSS-ленте: {len(feed["entries"])}')

        added_list = self.get_rss_item_list(feed)

        # Завершить задание
        self.finish_source()

        return f"Добавлено постов: {len(added_list)}"


class Command(BaseCommand):
    help = 'Парсинг RSS'

    def add_arguments(self, parser):
        parser.add_argument('title', type=str)
        parser.add_argument('url', type=str)

    def handle(self, *args, **options):
        rssparser = RSSParser()
        # status = STATUS_NEW
        source = Source.objects.filter(url=options['url']).first()
        if source.status == STATUS_NEW:
            PeriodicTask.objects.create(
                name='task_rss_loader',
                task='task_rss_loader',
                interval=IntervalSchedule.objects.get(every=120, period='seconds'),
                start_time=timezone.now(),
            )

        if source.status == STATUS_READY:
            logger.info('[*] Source {} status -> {}'.format(source.title, source.status))

        source.status = STATUS_READY
        source.refresh_from_db()
        logger.info('[*] Source {} status -> {}'.format(source.title, source.status))

        rssparser.parse_all()
