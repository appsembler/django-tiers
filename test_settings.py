from workbench.settings import *  # Make testing easier by mocking ROOT_URLCONF

from django.conf.global_settings import LOGGING  # Fix a workbench undesired behaviour

DEBUG = True
TEST_MODE = True
TEST_ROOT = "tests"
TRANSACTIONS_MANAGED = {}
USE_TZ = False
TIME_ZONE = {}
SECRET_KEY = 'SHHHHHH'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': u'test.db'.format(TEST_ROOT)
    },
}

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'workbench',
    'fake_organizations',
    'tiers',

)

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TIERS_ORGANIZATION_MODEL = 'fake_organizations.Organization'
TIERS_EXPIRED_REDIRECT_URL = "/site-deactivated"
