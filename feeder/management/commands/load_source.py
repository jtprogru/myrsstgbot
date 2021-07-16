from datetime import datetime
from django.conf import settings
from django.utils import timezone
from logging import getLogger
import os
from pprint import pprint
from typing import List

from django.core.management import BaseCommand, CommandError
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from feeder.constants import STATUS_NEW
from feeder.models import Source

from ruamel.yaml import YAML


logger = getLogger(__name__)


def log_errors(f):
    """Простейший декоратор-логгер"""
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            logger.error(error_message)
            raise e

    return inner


@log_errors
def datetime_parse(date_string: str) -> datetime:
    """Универсальный парсер даты и времени"""
    return dateparser.parse(date_string)


@log_errors
def yaml_loader(file_path) -> dict:
    """Загружаем данные из YAML"""
    yaml = YAML()
    with open(file_path, 'r') as f:
        return yaml.load(f.read())


class Loader:
    """
    Класс загрузки из YAML всех новых 
    """
    def __init__(self, src_file: str = 'sources.yaml'):
        self.source_file = src_file

    def check_source(self, src_file: str):
        """Проверяем существование файла"""
        if src_file:
            if os.path.exists(os.path.join(settings.BASE_DIR, src_file)):
                return os.path.join(settings.BASE_DIR, src_file)
        return None

    @log_errors
    def load(self):
        """Загрузка данных в БД"""
        yaml_data = yaml_loader(self.check_source(self.source_file))

        if "feeds" not in yaml_data:
            msg = f'В файле не объявлен ключ "feeds"'
            logger.info(msg)
            return msg


        logger.info(f"Источников в файле: {len(yaml_data['feeds'])}")

        for source in yaml_data['feeds']:
            try:
                Source.objects.update_or_create(
                    title=source['title'],
                    url=source['url'],
                )
            except Exception as e:
                logger.info(e)

        logger.info(f'Всего RSS-лент добавлено или обновлено записей: {len(yaml_data["feeds"])}')

        return f'Всего RSS-лент добавлено или обновлено записей: {len(yaml_data["feeds"])}'



class Command(BaseCommand):
    help = 'Загрузка RSS'

    def add_arguments(self, parser):
        parser.add_argument('src_file', type=str)

    def handle(self, *args, **options):
        loader = Loader(src_file=options['src_file'])

        loader.load()

