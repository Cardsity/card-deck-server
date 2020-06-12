#!/usr/bin/env sh

# Automatic migrate
if [ -n "$DJANGO_AUTOMATIC_MIGRATE" ] ; then
    python manage.py migrate --settings carddeckserver.settings.prod
fi

# Create superuser if parameters were supplied
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    python manage.py createsuperuser --settings carddeckserver.settings.prod --no-input
fi

# Collect static files
if [ -n "$DJANGO_COLLECTSTATIC" ] ; then
    python manage.py collectstatic --settings carddeckserver.settings.prod --noinput
fi

# Run the server
gunicorn carddeckserver.wsgi --bind 0.0.0.0:8020 --workers 3