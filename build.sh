#!/usr/bin/env bash
set -o errexit

uv pip install --system -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
