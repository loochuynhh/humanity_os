#!/bin/bash
# Cài dependencies hệ thống
apt-get update
apt-get install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev python3-dev fonts-liberation

# Cài requirements.txt
pip install -r /home/site/wwwroot/requirements.txt

# Chạy migrations
python /home/site/wwwroot/manage.py migrate

# Khởi động Gunicorn
gunicorn --bind=0.0.0.0:$PORT humanity_os.wsgi