#!/bin/bash
# Kích hoạt virtual environment từ artifact
source /home/site/wwwroot/venv/bin/activate

# Cài dependencies hệ thống (phòng trường hợp cần cho runtime)
apt-get update
apt-get install -y fonts-liberation

# Chạy migrations
python /home/site/wwwroot/manage.py migrate

# Khởi động Gunicorn
gunicorn --bind=0.0.0.0:$PORT humanity_os.wsgi