#!/bin/bash

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

# configure gunicorn

pip install gunicorn

current_dir=$(pwd)

me=$(whoami)

# create the ghydra.service

echo "[Unit]" > ghydra.service
echo "Description=Gunicorn instance to serve myproject" >> ghydra.service
echo "After=network.target" >> ghydra.service
echo " "
echo "[Service]" >> ghydra.service
echo "User=${me}" >> ghydra.service
echo "Group=www-data" >> ghydra.service
echo "WorkingDirectory=${current_dir}" >> ghydra.service
echo "ExecStart=${current_dir}/start-gunicorn.sh" >> ghydra.service
echo " "
echo "[Install]" >> ghydra.service
echo "WantedBy=multi-user.target" >> ghydra.service

# copy the ghydra.service file to the systemctl folder
sudo cp ghydra.service /etc/systemd/system/ghydra.service

# make sure our startup script is executable
chmod +x start-gunicorn.sh

