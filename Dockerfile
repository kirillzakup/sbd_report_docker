# Универсальный Dockerfile для Render
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Системные библиотеки для reportlab + шрифты
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

# Копируем весь репозиторий (чтобы не зависеть от путей)
COPY . /app/

# Ставим зависимости напрямую (без pyproject/requirements)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
      flask \
      pytelegrambotapi \
      reportlab \
      gunicorn

EXPOSE 5000

# Универсальный запуск:
# если есть подпапка DiscordQuoteBot/DiscordQuoteBot с app.py — запускаем из неё,
# иначе запускаем из корня
CMD bash -lc '\
  if [ -f "/app/DiscordQuoteBot/DiscordQuoteBot/app.py" ]; then \
    cd /app/DiscordQuoteBot/DiscordQuoteBot; \
  else \
    cd /app; \
  fi; \
  exec gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT:-5000} app:app \
'
