# coding=utf-8
from typing import Optional

from django.conf import settings

import requests


class BotException(BaseException):
    """
    Класс исключений для обертки над ботом
    """
    pass


class Bot:
    """
    Простая обертка над Telegram API
    """
    def __init__(self, bot_token: str = settings.TG_BOT_TOKEN):
        self._bot_token = bot_token
        self._base_url = f'https://api.telegram.org/bot{self._bot_token}/'

    def request(self, method: str) -> Optional[dict]:
        global res
        try:
            res = requests.get(self._base_url + method)
            return res.json()
        except:
            raise BotException(f"Во время запроса {method} произошла ошибка\n\t{res.text}")

    def getMe(self):
        _bot = self.request(method=self.getMe.__name__)


bot = Bot()
