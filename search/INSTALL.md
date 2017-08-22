Search
======

# Prerequisite

Make sure Experchat application has been setup. And MySQL database hase been setup.

ExperChat App: https://bitbucket.org/avihoffer/ec_python/src/master/README.md

# Search

## Clone the Source

    # Clone Search repository
    git clone git@bitbucket.org:avihoffer/ec_python_search.git

## Configure It

    # Go to search directory
    cd search

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

## Run search service

    ./manage.py runserver 8090

# Celery: Distributed Task Queue

## Setup Broker Queue

    sudo rabbitmqctl add_vhost search
    sudo rabbitmqctl set_permissions -p search guest ".*" ".*" ".*"

## Running development worker

    celery -A config worker -l info

# Solr Installation/Configuration

## Install jdk 9 and jre 9

    sudo apt -y install openjdk-9-jdk openjdk-9-jre

## Install apache solr-6.5.0
    cd /opt
    sudo wget http://mirror.fibergrid.in/apache/lucene/solr/6.5.0/solr-6.5.0.tgz
    sudo tar -xvf solr-6.5.0.tgz

    # Renaming and removing unwanted files from system
    sudo mv solr-6.5.0 solr
    sudo rm -rf solr-6.5.0.tgz
    cd /opt/solr

## Start/stop/restart solr engine
    sudo bin/solr start
    sudo bin/solr stop
    sudo bin/solr restart
    sudo bin/solr status

## Map MySQL associated tables to Solr core

    sudo bin/solr create -c experts
    sudo bin/solr create -c tags

    Check on http://localhost:solr-port{8983(default )}/solr/#/users

    # Install Java Connector for MySQL and remove unwanted files from system
    sudo apt-get install libmysql-java
    sudo mkdir/opt/solr/contrib/dataimporthandler/lib/
    sudo ln -s /usr/share/java/mysql.jar /opt/solr/contrib/dataimporthandler/lib/mysql.jar

    # Edit /opt/solr/server/solr/experts/core.properties and add database informations.
    MYSQL_HOSTNAME=localhost
    MYSQL_PORT=3306
    MYSQL_DB_NAME=ec_db
    MYSQL_USERNAME=ec_user
    MYSQL_PASSWORD=ec_password

    # Edit /opt/solr/server/solr/tags/core.properties and add database informations.
    MYSQL_HOSTNAME=localhost
    MYSQL_PORT=3306
    MYSQL_DB_NAME=ec_db
    MYSQL_USERNAME=ec_user
    MYSQL_PASSWORD=ec_password

    # Copy the schema/db-data-config/solrconfig XMLs to corename/conf folder
    sudo cp /home/experchat/search/config/solr/expert/schema.xml /opt/solr/server/solr/experts/conf
    sudo cp /home/experchat/search/config/solr/expert/data-config.xml /opt/solr/server/solr/experts/conf
    sudo cp /home/experchat/search/config/solr/expert/solrconfig.xml /opt/solr/server/solr/experts/conf
    sudo cp /home/experchat/search/config/solr/tags/schema.xml /opt/solr/server/solr/tags/conf
    sudo cp /home/experchat/search/config/solr/tags/data-config.xml /opt/solr/server/solr/tags/conf
    sudo cp /home/experchat/search/config/solr/tags/solrconfig.xml /opt/solr/server/solr/tags/conf
    sudo rm /opt/solr/server/solr/experts/conf/managed-schema

# MongoDB Server

    sudo apt install mongodb-server
    sudo mkdir -p /data/db/
    sudo service mongodb restart
