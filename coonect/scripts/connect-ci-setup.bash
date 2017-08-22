#!/bin/bash

ENV_SETTING=ci
ENV_DECRYPTION_PASSWD=<ci_config_decreption_password>
REPO_USERNAME=<common_repo_user>
REPO_PASSWORD=<common_repo_password>

git clone https://$REPO_USERNAME:$REPO_PASSWORD@bitbucket.org/avihoffer/ec_python_connect.git connect
cd connect/
git checkout -f origin/$1

docker build --rm --build-arg env_setting=$ENV_SETTING --build-arg env_decryption_passwd=$ENV_DECRYPTION_PASSWD --build-arg common_repo_password=$REPO_PASSWORD --build-arg common_repo_user=$REPO_USERNAME -t connect .

docker run connect ./manage.py check
if [ $? -ne 0 ]
then
    echo "Django check failed."
    exit 1
fi

docker run connect pytest --no-cov
if [ $? -ne 0 ]
then
    echo "Python Test Failed."
    exit 1
fi

docker run -d -p 8222:8222 connect
