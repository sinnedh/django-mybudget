import os
from mybudget.settings.base import *

ALLOWED_HOSTS = ['django-mybudget.herokuapp.com']

BOWER_COMPONENTS_ROOT = '/app/components/'

import dj_database_url
DATABASES['default'] = dj_database_url.config()

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_URL', None),
}

INSTALLED_APPS = INSTALLED_APPS + (
    'raven.contrib.django.raven_compat',
)

LOGGING['handlers']['sentry'] = {
    'level': 'WARNING',
    'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
}

LOGGING['root']['handlers'].append('sentry')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': os.environ.get('MEMCACHEDCLOUD_SERVERS', None)
    }
}
