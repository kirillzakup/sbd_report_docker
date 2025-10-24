# Docker + Render: полный проект

В корне уже добавлены:
- `Dockerfile` (без heredoc, через gunicorn)
- `.dockerignore`
- `render.yaml`

Ожидаемая структура после распаковки:
```
DiscordQuoteBot-Dockerized/
├─ DiscordQuoteBot/
│  └─ DiscordQuoteBot/
│     ├─ app.py
│     ├─ index.html
│     ├─ pyproject.toml
│     └─ ... (остальные файлы)
├─ Dockerfile
├─ .dockerignore
└─ render.yaml
```

## Render
1) New → Web Service → выбери **Docker**.
2) Залей этот репозиторий/архив (Dockerfile в корне).
3) Environment → `TELEGRAM_BOT_TOKEN` (токен бота).
4) Health Check Path: `/`.
5) Deploy.

## Локально
```bash
docker build -t quote-bot .
docker run -p 5000:5000 -e TELEGRAM_BOT_TOKEN=xxx quote-bot
# http://localhost:5000/
```
