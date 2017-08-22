ExperChat
=========

## About

ExperChat is a game changing business model that has the potential to disrupt the way knowledge is leveraged and monetized in this
interconnected world. It is a platform and a set of user apps that connects individuals to relevant subject matter information feeds from public and private media sources. These sources provides a rich multimedia experience of relevant information to the user as well as direct access to experts of those feeds. Access to these experts are private, one-on-one sessions, for Q&A, mentoring and coaching. Experts can now easily monetize their content, knowledge and expertise directly to users. By notifying their existing Social Media Followers and leveraging our marketing platform, experts now get paid for what was once free information and content. The real time access to information feeds and a secure easy way to connect to specific experts, in real-time, will make this app the go-to-app for every day.

## Prerequisites

- Linux (Preferably Ubuntu)
- Python 3.5+
- Python-pip
- Python-virtualenv
- MySQL 5.7.16

## Installation With Docker

#### Install Docker

    https://docs.docker.com/engine/installation/

#### Clone the Source

    # Clone ExperChat repository
    git clone git@bitbucket.org:avihoffer/ec_python.git experchat

#### Build it

    cd experchat

    # Set environment variables
    ENV_SETTING=dev
    ENV_DECRYPTION_PASSWD=dev
    REPO_USERNAME=<common_repo_user>
    REPO_PASSWORD=<common_repo_password>

    # Build docker image
    docker build --rm --build-arg env_setting=$ENV_SETTING --build-arg env_decryption_passwd=$ENV_DECRYPTION_PASSWD --build-arg common_repo_password=$REPO_PASSWORD --build-arg common_repo_user=$REPO_USERNAME -t experchat .

    # Run docker container
    docker run -d -p 8000:8000 experchat

## Manual Installation

See INSTALL.md
