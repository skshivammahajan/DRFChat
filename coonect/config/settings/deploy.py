from config.settings.base import *

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]
