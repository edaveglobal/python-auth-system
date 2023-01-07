#!/bin/bash

SUPERUSER_EMAIL=${DJANGO_SUPERUSER_EMAIL:-"gathpay@gmail.com"}
cd /app/

/opt/venv/bin/python ./auth_system/manage.py migrate --noinput
/opt/venv/bin/python ./auth_system/manage.py createsuperuser --email $SUPERUSER_EMAIL --noinput || true