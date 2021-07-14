from django.core.management import BaseCommand
from django.conf import settings

import feedparser


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
def parse(url: str):
    return feedparser.parse(url)


class Command(BaseCommand):
    help = 'Парсинг RSS'

    def handle(self, *args, **options):
        feed = parse(settings.RSS_URL)
        print(f"Последняя запись:\n{feed['entries'][0]['title']}\n{feed['entries'][0]['link']}")
