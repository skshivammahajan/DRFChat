Search
======

## About
Search is application to allow users to search experts and tags.

## Prerequisites

- Linux (Preferably Ubuntu)
- Python 3.5+
- pip
- virtualenv
- MySQL 5.7.16
- Java-9

## Installation With Docker

#### Install Docker

    https://docs.docker.com/engine/installation/

#### Clone the Source

    # Clone Search repository
    git clone git@bitbucket.org:avihoffer/ec_python_search.git search

#### Build it

    cd search

    # Set environment variables
    ENV_SETTING=dev
    ENV_DECRYPTION_PASSWD=dev
    REPO_USERNAME=<common_repo_user>
    REPO_PASSWORD=<common_repo_password>

    # Build docker image
    docker build --rm --build-arg env_setting=$ENV_SETTING --build-arg env_decryption_passwd=$ENV_DECRYPTION_PASSWD --build-arg common_repo_password=$REPO_PASSWORD --build-arg common_repo_user=$REPO_USERNAME -t search .

    # Run docker container
    docker run -d -p 8333:8333 search

## Manual Installation

See INSTALL.md
