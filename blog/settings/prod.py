from .base import *


DEBUG = False

ALLOWED_HOSTS = ['',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_name',
        'USER': 'db_user_name',
        'PASSWORD': 'db_password',
        'HOST': 'db_host',
        'PORT': 'db_port',
    }
}

import django_heroku
django_heroku.settings(locals())