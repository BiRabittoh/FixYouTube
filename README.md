# FixYouTube
Embed YouTube videos on Telegram, Discord and more!

## How to use:
Replace `www.youtube.com` or `youtu.be` with `y.outube.duckdns.org` to fix embeds for short videos.

![Demo](https://github.com/BiRabittoh/FixYouTube/assets/26506860/af3e9691-8c98-47e5-90e3-e5ebb1ba533f)

## Instructions (Docker)

### With reverse proxy
Copy the template config file and make your adjustments. My configuration is based on [DuckDNS](http://duckdns.org/) but you can use whatever provider you find [here](https://docs.linuxserver.io/general/swag#docker-compose).
```
cp docker/swag.env.example docker/swag.env
nano docker/swag.env
```

Finally: `docker-compose up -d`.

### Without reverse proxy
Simply run:
```
docker run -d -p 1111:80 --name fixyoutube --restart unless-stopped ghcr.io/birabittoh/fixyoutube:main
```

## Instructions (local)

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
