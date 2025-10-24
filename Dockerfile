FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
RUN apt-get update && apt-get install -y --no-install-recommends         build-essential libfreetype6-dev libjpeg-dev zlib1g-dev         libxext6 libxrender1 libfontconfig1 fonts-dejavu-core      && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY DiscordQuoteBot/DiscordQuoteBot/pyproject.toml /app/pyproject.toml
RUN python - <<'PY'import tomllib, pathlibdeps = tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']pathlib.Path('requirements.txt').write_text('\n'.join(deps))PY
RUN pip install --upgrade pip && pip install -r requirements.txt gunicorn
COPY DiscordQuoteBot/DiscordQuoteBot/ /app/
EXPOSE 5000
CMD ["bash", "-lc", "exec gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT:-5000} app:app"]
