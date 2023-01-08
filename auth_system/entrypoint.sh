#!/bin/bash
APP_PORT=${PORT:-8000}

# /opt/venv/bin/python manage.py collectstatic --noinput
/opt/venv/bin/python manage.py migrate --noinput
/opt/venv/bin/gunicorn  --bind "0.0.0.0:${APP_PORT}" \
         --workers=3 --worker-class=gevent \
         --access-logfile '-' --error-logfile '-' --capture-output \
         auth_system.wsgi:application