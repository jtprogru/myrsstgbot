from django.db import models

from .constants import STATUS_NEW, STATUS_RUNNING, STATUS_READY, POSTED_NO, POSTED_YES


class Source(models.Model):
    title = models.TextField(
        verbose_name='Название источника',
        unique=True,
    )
    url = models.URLField(
        verbose_name='Ссылка на источник',
        unique=True,
    )
    status = models.IntegerField(
        verbose_name='Статус обработки',
        choices=(
            (STATUS_NEW, 'Новое'),
            (STATUS_RUNNING, 'Запущено'),
            (STATUS_READY, 'Готово'),
        ),
        default=STATUS_NEW,
    )

    def __str__(self):
        return f'#{self.pk} {self.title}'

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Источник'
        verbose_name_plural = 'Источники'


class RSSItem(models.Model):
    """
    Модель записи из RSS-ленты
    """
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")
    link = models.URLField(max_length=512, unique=True, verbose_name="Ссылка на статью")
    pub_date = models.DateTimeField(verbose_name="Дата публикации")
    description = models.TextField(verbose_name="Описание")
    posted = models.IntegerField(
        verbose_name='Отправлено в TG',
        choices=(
            (POSTED_NO, 'Нет'),
            (POSTED_YES, 'Да'),
        ),
        default=POSTED_NO,
    )

    def __str__(self):
        return f"{self.id} | {self.title} | {self.pub_date}"

    class Meta:
        ordering = ['pub_date']
        verbose_name = "RSS-запись"
        verbose_name_plural = "RSS-записи"
