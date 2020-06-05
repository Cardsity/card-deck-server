#!/usr/bin/env bash

# Create superuser if parameters were supplied
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --no-input
fi

# Collect static files
if [ -n "$DJANGO_COLLECTSTATIC" ] ; then
    python manage.py collectstatic --settings carddeckserver.settings.prod --noinput
fi

# Automatic migrate
if [ -n "$DJANGO_AUTOMATIC_MIGRATE" ] ; then
    python manage.py migrate --settings carddeckserver.settings.prod
fi

# Run the server
gunicorn carddeckserver.wsgi --user www-data --bind 0.0.0.0:8010 --workers 3 &
nginx -g "daemon off;"