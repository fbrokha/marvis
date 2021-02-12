#!/bin/bash -e

docker build -t osmhpi/marvis -f docker/Dockerfile .

cd examples

docker-compose build
docker-compose up -d

docker run --rm \
    --net host --pid host --userns host --privileged \
    -v /var/run/docker.sock:/var/run/docker.sock:ro \
    -v $PWD:/examples -w /examples \
    osmhpi/marvis ./basic_example.py

docker-compose down
