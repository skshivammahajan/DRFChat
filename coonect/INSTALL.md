Connect
=========

# Prerequisite

Make sure Experchat application has been setup. And MySQL database hase been setup.

ExperChat App: https://bitbucket.org/avihoffer/ec_python/src/master/README.md

# Connect

## Clone the Source

    # Clone Connect repository
    git clone git@bitbucket.org:avihoffer/ec_python_connect.git connect

## Configure It

    # Go to connect directory
    cd connect

    # Virtual Envirnoment and requirements
    virtualenv -p /usr/bin/python3.5 env
    source env/bin/activate
    pip install -r requirements/common.txt
    pip install -r requirements/dev.txt

## Project and Database Configuartion Settings

    # Edit desired configurations in config/settings/local.py i.e. STATICFILES_DIRS
    cp config/settings/local.example.py config/settings/local.py
    chmod o-rwx config/settings/local.py
    editor config/settings/local.py

Example:

        from config.settings.dev import *

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': 'experchat_dev',
                'USER': 'experchat',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '',
            }
        }

## Validate configurations

    ./manage.py check

## Migrate Database

    ./manage.py migrate

## Run connect service

    ./manage.py runserver 8080

# Celery: Distributed Task Queue

## Setup Broker Queue

    sudo rabbitmqctl add_vhost connect
    sudo rabbitmqctl set_permissions -p connect guest ".*" ".*" ".*"

## Running development worker

    celery -A config worker -l info
