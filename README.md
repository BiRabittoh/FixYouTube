# FixYouTube
Embed YouTube videos on Telegram, Discord and more!

## Docker
```
docker-compose up -d
```

### Debug
```
poetry install
poetry run flask --app fixyoutube run --port 1111 --debug
```

### Production
```
poetry install --with prod
poetry run waitress-serve --port 1111 fixyoutube:app
```
