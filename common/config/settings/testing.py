"""
Settings for test environment.
"""
from config.settings.local import *

DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_URL = '/media/'

# To prevent sending emails
# https://docs.djangoproject.com/en/1.10/topics/email/#dummy-backend
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Causes API to send info in API response, instead of Email or SMS etc. for testing automation.
TEST_MODE = True
