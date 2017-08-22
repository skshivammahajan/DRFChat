from config.settings.base import *

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True

AUTH_SIGNING_KEY = '(#@+z+i1op1+hy=5(e4^wi%x*u4rh^paloyhp$i)m1ro@iac4!'

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

REST_FRAMEWORK.update({
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'experchat.authentication.TokenAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'experchat.renderers.EcJSONRenderer',
    ),
})
