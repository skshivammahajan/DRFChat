# Set the base image to use to Ubuntu
FROM ubuntu:16.04
ARG env_decryption_passwd
ARG common_repo_user
ARG common_repo_password
ARG common_repo_branch
ARG env_setting

# set the env variable from the build args
ENV ENV_DECRYPTION_PASSWD $env_decryption_passwd
ENV COMMON_REPO_USER $common_repo_user
ENV COMMON_REPO_PASSWORD $common_repo_password
ENV COMMON_REPO_BRANCH $common_repo_branch
ENV ENV_SETTING $env_setting

# add user
RUN adduser --disabled-password --disabled-login --gecos "Experchat" experchat

# meke the code directory
RUN mkdir /home/experchat/experchat

ADD . /home/experchat/experchat/

# Update the default application repository sources list
RUN apt-get update && apt-get -y upgrade

# Install the required packages
RUN apt install -y build-essential git libffi-dev python-docutils pkg-config python3-dev redis-server python3-pip

RUN openssl des3 -d -in /home/experchat/experchat/config/settings/$ENV_SETTING -out /home/experchat/experchat/config/settings/local.py -pass pass:$ENV_DECRYPTION_PASSWD

# make python3.5 as defualt python
RUN rm -r /usr/bin/python
RUN ln -s /usr/bin/python3.5 /usr/bin/python

# install the mysql and mysql-client
RUN apt-get install -y mysql-client libmysqlclient-dev

# Install av library dependencies
RUN apt-get install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev

# Upgrade pip
RUN pip3 install -U pip

# Install the commom dependency # mount to local dir
RUN pip3 install git+https://$COMMON_REPO_USER:$COMMON_REPO_PASSWORD@bitbucket.org/avihoffer/ec_python_common.git@$COMMON_REPO_BRANCH

# Install the requirments of the project
RUN pip3 install -r /home/experchat/experchat/requirements.txt
RUN pip3 install -r /home/experchat/experchat/requirements/testing.txt

# base directory to execute the Commands
WORKDIR /home/experchat/experchat

RUN ./manage.py migrate

RUN ./manage.py loaddata fixtures/default.json

EXPOSE 8000

CMD gunicorn config.wsgi:application --name experchat --workers 2 --bind=0.0.0.0:8000 --max-requests 200
