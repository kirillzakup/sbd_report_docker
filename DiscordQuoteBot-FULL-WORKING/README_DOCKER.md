# Полностью рабочий проект (с сохранёнными настройками бота)

Этот комплект НЕ меняет твоё `app.py`. Вместо gunicorn используется `run.py`, который:
- находит `app.py`,
- запускает `bot.infinity_polling()` в фоне (если есть `bot` и токен),
- стартует Flask на `$PORT`.

## Что нужно сделать
1) На Render добавь переменную окружения:
   - Key: `TELEGRAM_BOT_TOKEN`
   - Value: токен из @BotFather
2) Деплой (Runtime: Docker).

## Локально
docker build -t quote-bot .
docker run -p 5000:5000 -e TELEGRAM_BOT_TOKEN=xxx quote-bot
# http://localhost:5000/

Если когда-нибудь решишь вернуться к gunicorn — можно, но тогда polling в __main__ не сработает.
С `run.py` мы сохраняем поведение Replit один-в-один.
