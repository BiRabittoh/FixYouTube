# FixYouTube
Embed YouTube videos on Telegram!

## Docker
```
docker-compose up -d
```

### Debug
```
poetry install
poetry run flask --app fxyoutube run --port 1111 --debug
```

### Production
```
poetry install --with prod
poetry run waitress-serve --port 1111 fxyoutube:app
```
