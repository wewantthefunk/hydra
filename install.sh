#!/bin/bash

# install dependencies
#   most of these are probably already on your system

sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y

sudo apt install python-is-python3 python3.10-venv -y

# create the python virtual environment
python -m venv hydra-env

source hydra-env/bin/activate

# install dependencies in the virtual environment
pip install cryptography
pip install flask
pip install flask_mail
pip install wheel
pip install jdcal
pip install stripe

# install the configuration for the the hydra application
python admin/install.py false

echo "Your Hydra server is ready to run"
echo "For development and testing purposes, you can execute the ./start-dev.sh script"
echo ""
echo "For a production environment, install gunicorn and nginx"
echo "  the ./install-gunicorn.sh script is included to aid in this on Debian based systems"
