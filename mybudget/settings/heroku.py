import os
from mybudget.settings.base import *

BOWER_COMPONENTS_ROOT = '/app/components/'

import dj_database_url
DATABASES['default'] = dj_database_url.config()

RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_URL', None),
}

INSTALLED_APPS = INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
)

