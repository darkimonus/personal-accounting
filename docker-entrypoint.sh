#!/bin/bash
set -e


if [ "$CONTAINER_TYPE" = "master" ]; then
    poetry run python manage.py collectstatic --noinput
    echo "collected static"
    poetry run python manage.py migrate | tee migration_logs.txt
    echo "migrated"
    if [ "$DEPLOYMENT_SERVER" = "False" ]; then
    poetry run gunicorn --bind 0.0.0.0:8000 $DJANGO_PROJECT_NAME.wsgi:application
    fi
    poetry run gunicorn --bind 0.0.0.0:80 $DJANGO_PROJECT_NAME.wsgi:application
fi

if [ "$CONTAINER_TYPE" = "worker" ]; then
    poetry run celery -A "$DJANGO_PROJECT_NAME" worker -l info -Q "$DJANGO_PROJECT_NAME"_queue --concurrency=3
fi

if [ "$CONTAINER_TYPE" = "beat" ]; then
    poetry run celery -A "$DJANGO_PROJECT_NAME" beat -l info
fi
