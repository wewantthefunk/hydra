#!/bin/bash

sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
sudo apt install nginx -y

# activate the virtual environment

source hydra-env/bin/activate

echo "from hydra import app" > hydra_gunicorn.py
echo "if __name__ == "__main__":" >> hydra_gunicorn.py
echo "    app.run()" >> hydra_gunicorn.py

# configure gunicorn

pip install gunicorn

port=$(jq -r '.port' private/port.json)

gunicorn --bind 0.0.0.0:${port} wsgi:app

read -p "Enter the domain for your Hydra server: " user_input
echo "You entered: ${user_input}"

current_dir=$(pwd)

echo ${current_dir}

#echo "server {" > /etc/nginx/sites/available/${user_input}
#echo "  listen 80;" >> /etc/nginx/sites/available/${user_input}
#echo "  localhost ${user_input} www.${user_input};" >> /etc/nginx/sites/available/${user_input}
#echo " " >> /etc/nginx/sites/available/${user_input}
#echo "  location / {" >> /etc/nginx/sites/available/${user_input}
#echo "    include proxy_params;" >> /etc/nginx/sites/available/${user_input}
#echo "    proxy_pass http://unix:${current_dir}/hydra.sock

sudo ln -s /etc/nginx/sites-available/hydra /etc/nginx/sites-enabled

sudo ufw allow 'Nginx Full'
