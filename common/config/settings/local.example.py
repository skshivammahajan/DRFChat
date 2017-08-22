"""
To Override settings for local machine.
"""
# Raven Configurations
# import raven

from config.settings.dev import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tmp/db/dev.sqlite3'),
    }
}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gg@**7tm4m4715a!4y6c^8pb@orl7+m=l^2ikkdnx_8p)7b((p'

#AWS S3 Configurations
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = "*******"
AWS_SECRET_ACCESS_KEY = "*******"
AWS_STORAGE_BUCKET_NAME = "*******"


RAVEN_CONFIG = {
    'dsn': 'https://b694689aaa5f4a4f9af4ca05c01edc25:ab0e895d5c2c44bfb585ae79c7acd66c@sentry.io/130363',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    #'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    'release': 'v0.1',
}

# Facebook Auth settings
FACEBOOK_APP_ID = '251660191938379'
FACEBOOK_APP_SECRET = 'f77f52ee39d2b2c0c71b5db3ce4a5240'
FACEBOOK_APP_FEED_LIMIT = 10

# Instagram Auth settings
INSTAGRAM_CLIENT_ID = 'dfc5dde0abbf43a7a12f71878b4859c6'
INSTAGRAM_SECRET_CODE = '442d30e40ea24c41bd736bfd5b135871'

# Google API Feeds Settings for You Tube Data
YOUTUBE_SEARCH_LIST_API_MINE_FLAG = 'true'
GOOGLE_APP_API_KEY = 'AIzaSyBM9w3sWGzQM7_Au3MC-WzkvBBR382Lhh4'
GOOGLE_SECRET_KEY = 'Bx_AO2xqOfFQYlA19pgpNOS4'
GOOGLE_APP_CLIENT_ID = '290582452967-4qdsc74f13kn9lddq0iee400dt9h2132.apps.googleusercontent.com'

# Email configurations
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = '**********'
EMAIL_HOST_PASSWORD = '**********'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "no-reply@experchat.com"
# To prevent sending emails
# https://docs.djangoproject.com/en/1.10/topics/email/#dummy-backend
# EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# Causes API to send info in API response, instead of Email or SMS etc. for testing automation.
TEST_MODE = False

# Twilio Settings
ACCOUNT_SID = '******'
AUTH_TOKEN = '******'
PHONE = "******"

# Front End URLs
USER_FRONTEND_URL = "https://experchatqauser.app.link/"
USER_VERIFICATION_EMAIL_URL = "59au1Wd5BB"
USER_PASSWORD_RESET_URL = "yBVmXLi5BB"
EXPERT_FRONTEND_URL = "https://expertchatqa.app.link/"
EXPERT_VERIFICATION_EMAIL_URL = "LcbsW3LZBB"
EXPERT_PASSWORD_RESET_URL = "0Zg11pVZBB"

# CACHE BACKEND
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Cache time to live is 15 minutes.
CACHE_TTL = 60 * 60

# Authenticate WordPress CMS APIs
WP_SUPER_ADMIN_TOKEN = 'wp-token'
WP_ALLOWED_IPS = ['127.0.0.1']

# Get Stream Settings for Feeds
STREAM_API_KEY = '****'
STREAM_API_SECRET = '****'

# encryption key for confidential fields like account number
CONFIDENTIAL_FIELD_ENCRYPTION_KEY = 'experchat'

# Enable/disable API root
ENABLE_API_ROOT = False
