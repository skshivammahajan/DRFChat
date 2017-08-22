"""
To Override settings for local machine.
"""
from config.settings.deploy import *

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

# WebRTC Server TokBox Configurations
TOKBOX_API_KEY = "****************"
TOKBOX_API_SECRET = "****************"
TOKBOX_LOCATION = "<IP_Address>"

# Realtime Message Publisher PubNub Configurations
PUBNUB_SUBSCRIBE_KEY = "****************"
PUBNUB_PUBLISH_KEY = "****************"
PUBNUB_SUBSCRIBE_KEY_USER = "****************"
PUBNUB_PUBLISH_KEY_USER = "****************"
PUBNUB_DEBUG_MODE = False

# Causes API to send info in API response, instead of Email or SMS etc. for testing automation.
TEST_MODE = False

# Raven Config
# import raven

RAVEN_CONFIG = {
    'dsn': 'https://9041fcf52e3f46d99504e07ec4734b55:d701f76ccc794c75b05e9a4ab5a71b3f@sentry.io/130366',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    # 'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    'release': 'v0.1',
}

ENABLE_API_ROOT = False

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

# Braintree Configurations
BRAINTREE_ENVIRONMENT = 'sandbox'
BRAINTREE_MERCHANT_ID = "********"
BRAINTREE_PUBLIC_KEY = "********"
BRAINTREE_PRIVATE_KEY = "********"

TEST_CARD_ID = 1
