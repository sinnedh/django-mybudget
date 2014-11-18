from __future__ import with_statement
from fabric.api import local


def clean_pyc(settings='mybudget.settings.development'):
    local('python manage.py clean_pyc --settings={}'.format(settings))


def collectstatic(settings='mybudget.settings.development'):
    clean_pyc(settings)
    local('python manage.py collectstatic --settings={}'.format(settings))


def runserver(settings='mybudget.settings.development'):
    clean_pyc(settings)
    local('python manage.py runserver --settings={}'.format(settings))


def migrate(settings='mybudget.settings.development'):
    clean_pyc(settings)
    local('python manage.py makemigrations --settings={}'.format(settings))
    local('python manage.py migrate --settings={}'.format(settings))


def test(settings='mybudget.settings.testing'):
    clean_pyc(settings)
    local('python manage.py test --failfast --settings={}'.format(settings))


def deploy(settings='mybudget.settings.production'):
    local('git push heroku master')
    local('heroku run python manage.py clean_pyc --settings={}'.format(settings))
    local('heroku run python manage.py collectstatic --settings={}'.format(settings))
#    local('heroku run python manage.py makemigrations --settings={}'.format(settings))
    local('heroku run python manage.py migrate --settings={}'.format(settings))
