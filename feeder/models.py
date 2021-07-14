from django.db import models

from .constants import STATUS_NEW, STATUS_RUNNING, STATUS_READY


class Task(models.Model):
    title = models.TextField(
        verbose_name='Название задания',
        unique=True,
    )
    url = models.URLField(
        verbose_name='Ссылка на раздел',
        unique=True,
    )
    status = models.IntegerField(
        verbose_name='Статус задания',
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
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class RSSItem(models.Model):
    """
    Модель записи из RSS-ленты
    """
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")
    link = models.URLField(unique=True, verbose_name="Ссылка на статью")
    pub_date = models.DateTimeField(verbose_name="Дата публикации")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return f"{self.id} | {self.title} | {self.pub_date}"

    class Meta:
        verbose_name = "RSS-запись"
        verbose_name_plural = "RSS-записи"
