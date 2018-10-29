from .base import *
import dj_database_url

DEBUG = config("DEBUG", default=True, cast=bool)

ALLOWED_HOSTS += ['web']

# Development Apps
INSTALLED_APPS += []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(default=config('DB_URL'))
}