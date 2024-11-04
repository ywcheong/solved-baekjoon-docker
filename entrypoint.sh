#!/bin/bash

# Check if the project directory is empty
if [ -z "$(ls -A /work)" ]; then
    echo "First-time setup: Configuring Git and cloning repository."

    chmod 600 ~/.ssh/id_rsa
    ssh-keyscan github.com >> ~/.ssh/known_hosts

    # Configure Git user
    git config --global user.name "${GIT_USER_NAME}"
    git config --global user.email "${GIT_USER_EMAIL}"

    # Clone the GitHub repository using the provided secret
    git clone git@github.com:${GITHUB_PROJECT_NAME}.git /root/work
fi

# Start a bash shell
exec "$@"
