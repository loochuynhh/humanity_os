if [ -f /home/site/wwwroot/venv/bin/activate ]; then
    source /home/site/wwwroot/venv/bin/activate
    echo "Activated virtual environment: $(which python)"
else
    echo "ERROR: Virtual environment not found at /home/site/wwwroot/venv/bin/activate"
    exit 1
fi

apt-get update
apt-get install -y fonts-liberation

/home/site/wwwroot/venv/bin/python /home/site/wwwroot/manage.py migrate

/home/site/wwwroot/venv/bin/gunicorn --bind=0.0.0.0:$PORT humanity_os.wsgi