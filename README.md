# myrsstgbot

Simple Django app for load posts from RSS and send to Telegram.

## For running

Clone:
```shell
git clone https://github.com/jtprogru/myrsstgbot.git
```

Configure:
```shell
cd core
touch .env
```
Place in `.env` this vars:
- `TG_BOT_TOKEN` – Telegramm bot token;
- `SECRET_KEY` – Django secret key;
- `DEBUG` – Debug flag;
- `DJANGO_ALLOWED_HOSTS` – Allowed hosts for Django (not used);
- `CELERY_BROKER` – Connection string to Redis;
- `CELERY_BACKEND` – Connection string to Redis;

Example:
```ini
TG_BOT_TOKEN="1234567890:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
SECRET_KEY="django-insecure-6$SuperSecretKEY"
DEBUG=1
DJANGO_ALLOWED_HOSTS="localhost 127.0.0.1 [::1]"
CELERY_BROKER=redis://redis:6379/0
CELERY_BACKEND=redis://redis:6379/0
```

Run:
```shell
docker compose up -d 
```
