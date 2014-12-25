from mybudget.settings.base import *

BOWER_COMPONENTS_ROOT = BASE_DIR

#DATABASE_URL: postgres://mtcoxkptamowqx:qAj3Woq0NlSCqjjADFKdwC2taV@ec2-54-163-255-191.compute-1.amazonaws.com:5432/dcpu7ln0efr0uj
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

