#!/bin/bash
APP_PORT=${PORT:-8000}

/opt/venv/bin/python manage.py makemigrations wallet --noinput
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm auth_system.wsgi:application --bind "0.0.0.0:${APP_PORT}"