#!/bin/bash

# install dependencies
#   most of these are probably already on your system

sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y

sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python-is-python3 python3.10-venv -y

# create the python virtual environment
python -m venv hydra-env

source hydra-env/bin/activate

# install dependencies in the virtual environment
pip install cryptography
pip install flask
pip install flask_mail
pip install wheel

# install the configuration for the the hydra application
python admin/install.py false
