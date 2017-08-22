#!/bin/bash

if [ $# -lt 1 ]
then
    echo "Usage: /path/to/deployment/script.bash <branch_name>"
    exit 1
fi

ENV_SETTING=<env_setting>
ENV_DECRYPTION_PASSWD=<env_config_decreption_password>
REPO_USERNAME=<common_repo_user>
REPO_PASSWORD=<common_repo_password>
COMMON_REPO_BRANCH=<common_repo_branch>

# Remove existing images
docker rmi $(docker images -q)

git clone https://$REPO_USERNAME:$REPO_PASSWORD@bitbucket.org/avihoffer/ec_python.git experchat
cd experchat/
git checkout -f origin/$1

docker build -f Dockerfile-celery --rm --build-arg env_setting=$ENV_SETTING --build-arg env_decryption_passwd=$ENV_DECRYPTION_PASSWD --build-arg common_repo_password=$REPO_PASSWORD --build-arg common_repo_user=$REPO_USERNAME --build-arg common_repo_branch=$COMMON_REPO_BRANCH -t experchat-celery .

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

# Uncommment below commands if only single server is running.
# docker stop CONTAINER $(docker ps -q)
# docker rm $(docker ps -a -q)

docker run -d experchat-celery

cd ..
rm -rf experchat
