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
        if bot_token is None:
            raise BotException(f'[ERROR] Идиот! Переменная "{settings.TG_BOT_TOKEN=}" ')
        self._bot_token = bot_token
        self._base_url = f'https://api.telegram.org/bot{self._bot_token}/'

    def request(self, method: str, payload: dict = None) -> Optional[dict]:
        global res
        try:
            res = requests.get(self._base_url + method, params=payload)
            return res.json()
        except:
            raise BotException(f"Во время запроса {method} произошла ошибка\n\t{res.text}")

    def get_me(self) -> Optional[dict]:
        me = self.request(method='getMe')
        if not me['ok']:
            raise BotException(f"[ERROR] Ой... Я не смог получить данные о себе...")
        return me

    def send_message(self, message: str, chat_id: str = settings.TG_ADMIN_ID) -> Optional[dict]:
        if chat_id is None:
            raise BotException(f'[ERROR] Идиот! Переменная "{settings.TG_ADMIN_ID=}" ')
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
        }

        result = self.request(method="sendMessage", payload=payload)

        if not result['ok']:
            raise BotException(f"[ERROR] Ой... Я не смог получить данные о себе...")
        return result


bot = Bot()
