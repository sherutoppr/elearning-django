from .base import *

DEBUG = False

ADMINS = (
    ('sherukhan', 'jnvh1233sheru@gmail.com'),
)
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'educa',                                       #name of database we create in postgres
        'USER' : os.environ.get('POSTGRES_USER'),
        'PASSWORD' : os.environ.get('POSTGRES_PASS'),
        'HOST' : 'localhost',
    }
}