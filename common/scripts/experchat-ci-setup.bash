#!/bin/bash

MYSQL_ROOT_USER=root
MYSQL_ROOT_PASSWORD=<root_password>
MYSQL_CI_DATABASE=experchat_ci
ENV_SETTING=ci
ENV_DECRYPTION_PASSWD=<ci_config_decreption_password>
REPO_USERNAME=<common_repo_user>
REPO_PASSWORD=<common_repo_password>

docker stop CONTAINER $(docker ps -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)

mysqladmin -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD drop $MYSQL_CI_DATABASE -f
mysqladmin -u$MYSQL_ROOT_USER -p$MYSQL_ROOT_PASSWORD create $MYSQL_CI_DATABASE --default-character-set=utf8mb4


git clone https://$REPO_USERNAME:$REPO_PASSWORD@bitbucket.org/avihoffer/ec_python.git experchat
cd experchat/
git checkout -f origin/$1

docker build --rm --build-arg env_setting=$ENV_SETTING --build-arg env_decryption_passwd=$ENV_DECRYPTION_PASSWD --build-arg common_repo_password=$REPO_PASSWORD --build-arg common_repo_user=$REPO_USERNAME -t experchat .

docker run experchat ./manage.py check
if [ $? -ne 0 ]
then
    echo "Django check failed."
    exit 1
fi

docker run experchat pytest --no-cov
if [ $? -ne 0 ]
then
    echo "Python Test Failed."
    exit 1
fi

docker run -d -p 8000:8000 experchat
