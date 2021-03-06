# Generated by Django 3.2.5 on 2021-07-14 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RSSItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок статьи')),
                ('link', models.URLField(unique=True, verbose_name='Ссылка на статью')),
                ('pub_date', models.DateTimeField(verbose_name='Дата публикации')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
        ),
    ]
