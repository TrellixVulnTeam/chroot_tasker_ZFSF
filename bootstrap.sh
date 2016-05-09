#!/usr/bin/env bash

# New Python version with various improvements.
add-apt-repository ppa:fkrull/deadsnakes
apt update
apt -y install python3.5
apt -y install python3.5-dev

# Convenient for managing dependencies.
apt -y install python-virtualenv

# Install and configure virtualenvwrapper
pip install virtualenvwrapper
cat > /home/vagrant/.bashrc << "EOF"
export WORKON_HOME=/home/vagrant/.virtualenvs
mkdir -p $WORKON_HOME
sudo chown `whoami` $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
EOF
source /home/vagrant/.bashrc
