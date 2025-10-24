# Dockerfile that preserves Telegram bot settings by using run.py launcher
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libjpeg-dev \
    zlib1g-dev \
    libxext6 \
    libxrender1 \
    libfontconfig1 \
    fonts-dejavu-core \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy entire repo so we don't rely on specific paths
COPY . /app/

# Install dependencies explicitly (matches your pyproject), no reliance on pyproject/requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
      flask \
      pytelegrambotapi \
      reportlab

EXPOSE 5000

# Use our launcher that starts bot polling AND Flask, honoring $PORT
CMD ["python", "run.py"]
