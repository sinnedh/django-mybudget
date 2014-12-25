from mybudget.settings.base import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
}


INSTALLED_APPS += (
    'djangobower',
)


STATICFILES_FINDERS += (
    'djangobower.finders.BowerFinder',
)


BOWER_INSTALLED_APPS = (
   'fontawesome',
   'jquery',
   'bootstrap-datepicker',
   'bootstrap-select',
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, '../components/')
