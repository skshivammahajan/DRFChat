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

# Remove existing images
# docker rmi $(docker images -q)

git clone https://$REPO_USERNAME:$REPO_PASSWORD@bitbucket.org/avihoffer/ec_python_connect.git connect
cd connect/
git checkout -f origin/$1

docker build  -f Dockerfile-celery --rm --build-arg env_setting=$ENV_SETTING --build-arg env_decryption_passwd=$ENV_DECRYPTION_PASSWD --build-arg common_repo_password=$REPO_PASSWORD --build-arg common_repo_user=$REPO_USERNAME -t connect-celery .

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

# Uncommment below commands if only single server is running.
# docker stop CONTAINER $(docker ps -q)
# docker rm $(docker ps -a -q)

docker run -d connect-celery

cd ..
rm -rf connect
