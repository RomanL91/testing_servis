#!/usr/bin/env sh

python manage.py makemigrations --no-input
python manage.py migrate --no-input
exec gunicorn core.wsgi:application -b 0.0.0.0:8000 --reload
