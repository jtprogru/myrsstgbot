from django.db import models







class Message(models.Model):
    title = models.CharField(max_lenght=64, verbose_name='Заголовок отправляемого сообщения')
    body = models.CharField(max_lenght=256, verbose_name='Содержимое сообщения')
    created_date = models.DateTimeField(auto_now=True, verbose_name='Дата создания сообщения')
    publish_date = models.DateTimeField(verbose_name='Дата публикации')
    published = models.CharField(
        max_lenght=2,
        verbose_name='Статус публикации',
        choises=(
            (0, 'Нет'),
            (1, 'Да'),
        ),
        default=0,
    )
    channel = models.CharField(
        max_lenght=16,
        verbose_name='Куда опубликовано',
    )

    def __str__(self):
        return f'#{self.id} | {self.publish_date} | {self.title}'

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

