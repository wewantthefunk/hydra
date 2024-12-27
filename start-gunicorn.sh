#!/bin/bash

source hydra-env/bin/activate

port=$(jq -r '.port' private/port.json)

current_dir=$(pwd)

${current_dir}/hydra-env/bin/gunicorn --workers 3 --bind unix:ghydra.sock -m 007 wsgi:app