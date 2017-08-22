"""
To Override settings for local machine.
"""
from mongoengine import connect

from config.settings.deploy import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'tmp/db/dev.sqlite3'),
    }
}

MONGODB = {
    'db': 'test',
    'username': '',
    'password': '',
    'host': 'localhost',
    'port': 27017,
}
connect(**MONGODB)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gg@**7tm4m4715a!4y6c^8pb@orl7+m=l^2ikkdnx_8p)7b((p'

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

##Solr Search const
SOLR_PROTOCOL = 'http://'
SOLR_URL = "localhost"
SOLR_PORT = '8983'
SOLR_EXPERT_COLLECTION_NAME = 'experts'
SOLR_TAG_COLLECTION_NAME = 'tags'

SOLR_EXPERT_COLLECTION_URL = "{solr_protocol}{solr_url}:{solr_port}/solr/{solr_expert_collection_name}".format(
    solr_protocol=SOLR_PROTOCOL,
    solr_url=SOLR_URL,
    solr_port=SOLR_PORT,
    solr_expert_collection_name=SOLR_EXPERT_COLLECTION_NAME
)

SOLR_TAG_COLLECTION_URL = "{solr_protocol}{solr_url}:{solr_port}/solr/{solr_tag_collection_name}".format(
    solr_protocol=SOLR_PROTOCOL,
    solr_url=SOLR_URL,
    solr_port=SOLR_PORT,
    solr_tag_collection_name=SOLR_TAG_COLLECTION_NAME
)
