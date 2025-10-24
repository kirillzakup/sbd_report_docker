# Python 3.11 + system libs for reportlab
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

# Current structure: DiscordQuoteBot/DiscordQuoteBot/...
COPY DiscordQuoteBot/DiscordQuoteBot/pyproject.toml /app/pyproject.toml

# Generate requirements.txt from pyproject.toml (no heredoc) and install deps + gunicorn
RUN python -c "import tomllib, pathlib; deps = tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']; pathlib.Path('requirements.txt').write_text('\\n'.join(deps))" \
 && pip install --upgrade pip \
 && pip install -r requirements.txt gunicorn

# Copy app sources
COPY DiscordQuoteBot/DiscordQuoteBot/ /app/

EXPOSE 5000

# Flask app object 'app' is in app.py => app:app
CMD [ "bash", "-lc", "exec gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT:-5000} app:app" ]
