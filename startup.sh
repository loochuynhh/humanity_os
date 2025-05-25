#!/bin/bash

# Install system dependencies for face recognition
apt-get update
apt-get install -y cmake build-essential libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev

# Set Python path
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH

# Collect static files
python manage.py collectstatic --noinput --settings=humanity_os.settings_production

# Run migrations
python manage.py migrate --settings=humanity_os.settings_production

# Start gunicorn with increased timeout for face recognition processing
gunicorn --bind=0.0.0.0 --timeout 600 --workers=2 --max-requests=1000 --preload humanity_os.wsgi