## DEBUG
docker build -t docker_travel_request -f Dockerfile . && docker run -it -p 5000:5000 docker_travel_request:latest

## PRODUCTION
#docker build -t docker_qbox -f Dockerfile . && docker run -d -p 5000:5000 docker_qbox:latest