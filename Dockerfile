# ---- Base image ----
FROM python:3.12-slim

# ---- Set environment variables ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Install system packages ----
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libx11-dev \
    libgtk-3-dev \
    python3-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    curl \
    git \
    pkg-config \
    libmariadb-dev-compat \
    openssh-server \
    && rm -rf /var/lib/apt/lists/*

# ---- Configure SSH ----
RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# ---- Set workdir ----
WORKDIR /app

# ---- Copy requirements first ----
COPY requirements.txt /app/

# ---- Install dependencies ----
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ---- Copy project ----
COPY . /app

# ---- Activate virtual environment ----
ENV PATH="/opt/venv/bin:$PATH"

# ---- Expose ports ----
EXPOSE 8000 2222

# ---- Run migrations, collectstatic, and start Gunicorn ----
CMD ["sh", "-c", "/usr/sbin/sshd && python manage.py migrate && python manage.py collectstatic --noinput || exit 1 && gunicorn humanity_os.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 90"]