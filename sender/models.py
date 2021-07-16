from django.db import models

from . import constants


class ChannelType(models.Model):
    """
    Тип канала доставки сообщения
    Например Twitter, Telegram, Email, etc...
    """
    name = models.CharField(max_length=32, verbose_name='Имя типа канала доставки')
    uuid = models.UUIDField(auto_created=True, unique=True, verbose_name='UUID')
    channel = models.CharField(max_length=32, unique=True, verbose_name='Канал')
    connection_model = models.CharField(max_length=128, verbose_name='Как подключаться к каналу')

    class Meta:
        ordering = ['name']
        verbose_name = "Тип канала"
        verbose_name_plural = "Типы каналов"


class Channel(models.Model):
    """
    Канал доставки сообщения
    """
    title = models.CharField(max_length=64, verbose_name='Название канала')
    # channel_type = models.ForeignKey(ChannelType, on_delete=models.CASCADE, verbose_name='Тип канала')
    active = models.CharField(
        max_length=2,
        verbose_name='Использование канала',
        choices=constants.CHANNEL_ACTIVE_STATUS,
        default=constants.CHANNEL_ACTIVE_NO,
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Канал'
        verbose_name_plural = 'Каналы'


class Message(models.Model):
    """
    Сообщение для отправки
    """
    title = models.CharField(max_length=64, verbose_name='Заголовок отправляемого сообщения')
    body = models.CharField(max_length=256, verbose_name='Содержимое сообщения')
    created_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания сообщения')
    publish_date = models.DateTimeField(verbose_name='Дата публикации')
    published = models.CharField(
        max_length=2,
        verbose_name='Статус публикации',
        choices=constants.MESSAGE_PUBLISHED_STATUS,
        default=constants.MESSAGE_PUBLISHED_NO,
    )
    # channel = models.ManyToManyField(
    #
    #     verbose_name='Куда опубликовано',
    # )

    def __str__(self):
        return f'#{self.id} | {self.publish_date} | {self.title}'

    class Meta:
        ordering = ['created_date', 'publish_date']
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

