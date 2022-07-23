# coding=utf-8

class BotException(BaseException):
    """
    Класс исключений для обертки над ботом
    """
    pass


class Bot:
    """
    Простая обертка над Twitter API
    """
    def __init__(self, access_key: str, access_key_secret: str, connection_key: str, connection_key_secret: str):
        self._access_key = access_key
        self._access_key_secret = access_key_secret
        self._connection_key = connection_key
        self._connection_key_secret = connection_key_secret
