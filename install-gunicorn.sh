#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install nginx -y
sudo apt install jq -y

# activate the virtual environment

source hydra-env/bin/activate

# configure gunicorn

pip install gunicorn

port=$(jq -r '.port' private/port.json)

read -p "Enter the domain for your Hydra server: " user_input
echo "You entered: ${user_input}"

current_dir=$(pwd)

me=$(whoami)

echo ${current_dir}

echo "[Unit]" > ghydra.service
echo "Description=Gunicorn instance to serve myproject" >> ghydra.service
echo "After=network.target" >> ghydra.service
echo " "
echo "[Service]" >> ghydra.service
echo "User=${me}" >> ghydra.service
echo "Group=www-data" >> ghydra.service
echo "WorkingDirectory=${current_dir}" >> ghydra.service
echo "Environment=\"PATH=${current_dir}/hydra-env/bin\"" >> ghydra.service
echo "ExecStart=${current_dir}/start-gunicorn.sh" >> ghydra.service
echo " "
echo "[Install]" >> ghydra.service
echo "WantedBy=multi-user.target" >> ghydra.service

sudo cp ghydra.service /etc/systemd/system/ghydra.service

chmod +x start-gunicorn.sh

sudo systemctl stop ghydra

sudo systemctl daemon-reload

sudo systemctl start ghydra

sudo systemctl enable ghydra

#configure nginx

sudo echo "server {" > ghydra.nginx
sudo echo "  listen 80;" >> ghydra.nginx
sudo echo "  localhost ${user_input} www.${user_input};" >> ghydra.nginx
sudo echo " " >> ghydra.nginx
sudo echo "  location / {" >> ghydra.nginx
sudo echo "    include proxy_params;" >> ghydra.nginx
sudo echo "    proxy_pass http://unix:${current_dir}/ghydra.sock" >> ghydra.nginx
sudo echo "  }" >> ghydra.nginx
sudo echo "}" >> ghydra.nginx

sudo mv ghydra.nginx /etc/nginx/sites-available/ghydra

sudo ln -s /etc/nginx/sites-available/ghydra /etc/nginx/sites-enabled

sudo nginx -t

sudo systemctl restart nginx

sudo ufw allow 'Nginx Full'
