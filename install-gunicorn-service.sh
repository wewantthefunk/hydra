#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install nginx -y
sudo apt install jq -y

# activate the virtual environment

source hydra-env/bin/activate

# configure gunicorn

sudo pip install gunicorn

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

# start the service
sudo systemctl stop ghydra

sudo systemctl daemon-reload

sudo systemctl start ghydra

sudo systemctl enable ghydra

