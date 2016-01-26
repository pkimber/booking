# -*- encoding: utf-8 -*-
from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'temp.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

INSTALLED_APPS += ('debug_toolbar', )

# http://docs.celeryproject.org/en/2.5/django/unit-testing.html
CELERY_ALWAYS_EAGER = True
