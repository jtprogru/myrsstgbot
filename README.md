# myrsstgbot

Простое приложение на Django для получения постов и новостей через RSS и отправки в Telegram новостных сводок.

## Запуск

Клонировать:
```shell
git clone https://github.com/jtprogru/myrsstgbot.git
```

Создать `.env` файл с переменными окружения:
```shell
cd myrsstgbot
touch .env
```
Переменные в  `.env` файле:
- `TG_BOT_TOKEN` – Telegramm bot token;
- `SECRET_KEY` – Django secret key;
- `DEBUG` – Debug flag;
- `DJANGO_ALLOWED_HOSTS` – Allowed hosts for Django;
- `CELERY_BROKER` – Connection string to Redis;
- `CELERY_BACKEND` – Storage for results;
- `C_FORCE_ROOT` – Celery allow run as root;
- `SQL_ENGINE` – Движок подключения к БД;
- `SQL_DATABASE` – Имя БД;
- `SQL_USER` – Пользователь БД;
- `SQL_PASSWORD` – Пароль БД;
- `SQL_HOST` – Имя хоста с БД;
- `SQL_PORT` – Порт подключения к БД;
- `POSTGRES_USER` – Пользователь БД;
- `POSTGRES_PASSWORD` – Пароль БД
- `POSTGRES_DB` – Имя БД;
- `FEEDER_DEFAULT_SRC_FILE` – YAML'ик с источниками RSS;

Пример:
```ini
TG_BOT_TOKEN="1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SECRET_KEY="django-insecure-6$SuperSecretKEY"
DEBUG=1
DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"
CELERY_BROKER=redis://rediska:6379/0
CELERY_BACKEND=django-db
C_FORCE_ROOT=1
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=postgres
SQL_USER=postgres
SQL_PASSWORD=postgres
SQL_HOST=postgresql
SQL_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
FEEDER_DEFAULT_SRC_FILE=sources.yaml
```

Запуск в Docker:
```shell
docker compose up -d --build 
```

Создать суперюзера внутри контейнера:
```shell
docker compose exec app sh 
# внутри контейнера выполняется
pythno3 manage.py createsuperuser
```

## Наполнение источниками RSS

Отредактировать `sources.yaml`:
```yaml
---
feeds: # обязательный объект со списком RSS-лент
  - title: '@habr' # название RSS-ленты
    url: 'https://habr.com/ru/rss/all/all/?fl=en%2Cru&limit=100' # ссылка на RSS-ленту
  - title: '@jtprog' # название RSS-ленты
    url: 'https://jtprog.ru/index.xml' # ссылка на RSS-ленту
```

Импорт всех источников будет выполнен автоматически – расписание в файле `celery.py` в базовом модуле `core`:
```yaml
...
{
    'task_source_loader': {  # имя задачи
        'task': 'feeder.tasks.task_source_loader',  # откуда брать задачу - <app_name>.<tasks_file>.<func_name>
        'schedule': 60 * 30,  # интервал выполнения (в секундах)
    }
}
...
```

## Copyright

LICENSE: http://www.wtfpl.net

## Author
Savin Michael aka [@jtprogru](https://github.com/jtprogru)

WWW: https://jtprog.ru

Twitter: https://twitter.com/jtprogru

Telegram: https://t.me/jtprogru_channel

