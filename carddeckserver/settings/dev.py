from carddeckserver.settings.base import *
import os

# Settings in development should generally match between every developer so it is easy to fix errors

SECRET_KEY = '(lf2k+^@gd!%g_cn5(zod!mf(@#qfod2cl^2xxb4ho7*4bhp8^'
DEBUG = True
ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
