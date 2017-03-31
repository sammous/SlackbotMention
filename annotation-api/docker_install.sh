echo "-----------------------------------------"
echo "SentimentBot Docker builder"
echo "-----------------------------------------"

echo "[-->] Now building the Docker image..."

docker build -t annotation-api .

docker build -t annotation-bot -f Dockerfile_bot .

echo "DONE!"

echo "Stopping existing containers..."
docker stop annotation-api
docker stop annotation-bot
echo "containers STOPPED"

echo "Remove existing containers..."
docker rm annotation-api
docker rm annotation-bot
echo "containers REMOVED"

echo "Running Containers.."
docker run -d --name annotation-api -e "port=3000" -e "protocol=http" -p 3000:3000 annotation-api

#docker run -d --name annotation-ngrok -p 4040:4040 --link annotation-api wernight/ngrok ngrok http --subdomain=5859a96b annotation-api:3000

docker run -d --name annotation-bot annotation-bot bash -c 'source app_venv/bin/activate; python3 src/annotation/slackbotuser/botuser.py'

echo
echo "DONE!"
