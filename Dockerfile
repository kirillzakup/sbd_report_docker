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

# Копируем ВСЁ репо (чтобы не зависеть от структуры)
COPY . /app/

# Ставим зависимости напрямую
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
      flask \
      pytelegrambotapi \
      reportlab \
      gunicorn

EXPOSE 5000

# Автопоиск app.py и запуск gunicorn из нужной папки
CMD bash -lc '\
  APP_FILE=$(find /app -maxdepth 4 -type f -name app.py | head -n1); \
  if [ -z "$APP_FILE" ]; then \
    echo "❌ app.py не найден. Проверь структуру репозитория."; exit 1; \
  fi; \
  APP_DIR=$(dirname "$APP_FILE"); \
  echo "✅ Найден app.py: $APP_FILE"; \
  cd "$APP_DIR"; \
  # Если объект Flask называется не app, можно поменять на <имя>:app
  exec gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT:-5000} app:app \
'
