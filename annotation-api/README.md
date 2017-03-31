# Using Sentiment Annotation API

Tested on *Python 3.5*

## Database

The sentiment annotation API uses *MySQL*.
Run `database/annotation.sql` before to install the correct table.

Change then the correct credentials (VERIFICATION_TOKEN) in `/src/annotation/config/default.py`.

## Installation

To install it on `mention.b` using `ngrok` run the file `docker_install.sh`:


Build the API:
```
docker build -t annotation-api:2 .
```

Build the bot:
```
docker build -t annotation-bot:2 -f Dockerfile_bot .
```

Run containers:
```
docker run -it --rm --name annotation-api -e "port=3000" -e "protocol=http" -p 3000:3000 annotation-api:2

docker run -it -d -p 4040:4040 --link annotation-api wernight/ngrok ngrok http annotation-api:3000

docker run -d --name annotation-bot annotation-bot:2 bash -c 'source app_venv/bin/activate; python3 src/annotation/slackbotuser/botuser.py'
```


Where `annotation-api:2` is the name of the image containing the flask application, and `wernight/ngrok` is the name of the image containing ngrok.

## Issues

- One spotted issue is the delay in the scheduling, coming from the timezone of the container not matching *CET*.
- A specific parsing library from Mention was used, and therefore code needs to be updates so Resources can properly used requests.
