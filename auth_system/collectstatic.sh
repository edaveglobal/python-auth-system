#!/bin/bash
cd /app/
/opt/venv/bin/python auth_system/manage.py collectstatic --noinput
