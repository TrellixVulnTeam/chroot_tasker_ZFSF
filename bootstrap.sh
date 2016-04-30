#!/usr/bin/env bash

apt-get -y install python-virtualenv
pip install virtualenvwrapper
cat > /home/vagrant/.bashrc << "EOF"
export WORKON_HOME=/home/vagrant/.virtualenvs
mkdir -p $WORKON_HOME
sudo chown `whoami` $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh
EOF
source /home/vagrant/.bashrc
