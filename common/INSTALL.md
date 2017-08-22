ExperChat
=========

# Important Notes

This guide is long because it covers many cases and includes all commands you need.

This installation guide was created for and tested on **Ubuntu 16.04** operating systems.

The following steps have been known to work. Please **use caution when you deviate** from this guide. Make sure you don't violate any assumptions ExperChat makes about its environment.

# Overview

The  ExperChat installation consists of setting up the following components:

1. Packages / Dependencies
1. Database
1. ExperChat
1. Celery: Distributed Task Queue

## Packages / Dependencies

Run following commands

    sudo apt-get update
    sudo apt-get -y upgrade

**Note:** During this installation some files will need to be edited manually. If you are familiar with vim set it as default editor with the commands below. If you are not familiar with vim please skip this and keep using the default editor.

    # Install vim and set as default editor
    sudo apt-get install -y vim-gnome
    sudo update-alternatives --set editor /usr/bin/vim.gnome

Install the required packages

    sudo apt install -y build-essential git libffi-dev python-docutils pkg-config python3-dev python-dev python-virtualenv python-pip rabbitmq-server redis-server

Install the dependencies of PyAV package to create thumbnails of video

    # General dependencies
    sudo apt-get install -y python-dev pkg-config

    # Library components
    sudo apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev

# Database

    # Install the database packages
    sudo apt-get install -y mysql-server mysql-client libmysqlclient-dev

    # Login to MySQL
    mysql -u root -p

    # Create a user for ExperChat. (change $password to a real password)
    mysql> CREATE USER 'experchat'@'localhost' IDENTIFIED BY '$password';

    # Create the ExperChat development database
    mysql> CREATE DATABASE IF NOT EXISTS `experchat_dev` DEFAULT CHARACTER SET `utf8mb4` COLLATE `utf8mb4_unicode_ci`;

    # Grant the ExperChat user necessary permissopns on the table.
    mysql> GRANT ALL ON `experchat_dev`.* TO 'experchat'@'localhost';

    # Quit the database session
    mysql> \q

    # Try connecting to the new database with the new user
    sudo -u git -H mysql -u experchat -p -D experchat_dev


# ExperChat

## Clone the Source

    # Clone ExperChat repository
    git clone git@bitbucket.org:avihoffer/ec_python.git experchat

## Configure It

    # Go to ExperChat installation folder
    cd experchat

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

## Migrate Database & Seed Default Data

    ./manage.py migrate
    ./manage.py loaddata fixtures/default.json

## Create Superuser

    ./manage.py createsuperuser

## Run Server

    ./manage.py runserver

# Celery: Distributed Task Queue

## Setup Broker Queue

    sudo rabbitmqctl add_vhost experchat
    sudo rabbitmqctl set_permissions -p experchat guest ".*" ".*" ".*"

## Running development worker

    celery -A config worker -l info
