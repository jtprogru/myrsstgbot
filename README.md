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

Пример:
```ini
TG_BOT_TOKEN="1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SECRET_KEY="django-insecure-6$SuperSecretKEY"
DEBUG=1
DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"
CELERY_BROKER=redis://rediska:6379/0
CELERY_BACKEND=django-db
C_FORCE_ROOT=1
```

Запуск в Docker:
```shell
docker compose up -d 
```

Создать суперюзера можно локально (потребуется созданное виртуальное окружение), либо внутри контейнера:
```shell
source venv/bin/activate
python3 manage.py migrate
pythno3 manage.py createsuperuser
```

## Наполнение источниками RSS

Зайти в SQLite3 базу данных:
```shell
sqlite3 db.sqlite3
```

Импортировать базовые источники:
```sqlite
.read init.sql
.quit
```

## Copyright

LICENSE: http://www.wtfpl.net

AUTHOR: Savin Michael aka [@jtprogru](https://github.com/jtprogru)

WWW: https://jtprog.ru

Twitter: https://twitter.com/jtprogru

