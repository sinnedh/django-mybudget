from mybudget.settings.base import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, '../db.sqlite3'),
}

# self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
REDIS_URL = 'redis://localhost:6379'
