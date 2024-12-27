#!/bin/bash

python -m venv hydra

source hydra/bin/activate

pip install cryptography
pip install flask
pip install flask_mail

python admin/install.py false
