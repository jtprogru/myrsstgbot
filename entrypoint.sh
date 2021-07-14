#!/bin/sh

#python3 manage.py flush --no-input
python3 manage.py migrate
#python manage.py collectstatic --no-input --clear

exec "$@"
