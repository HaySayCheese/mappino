# coding=utf-8

from dev_settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test_(test)mappino-db',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    },
}
DATABASE_ROUTERS = []