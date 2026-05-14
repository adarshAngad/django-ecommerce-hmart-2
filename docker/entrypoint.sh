#!/bin/sh
set -eu
cd /app

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec gunicorn Annu.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers "${WEB_CONCURRENCY:-2}" \
  --threads "${GUNICORN_THREADS:-1}" \
  --access-logfile - \
  --error-logfile - \
  --capture-output
