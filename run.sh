#!/bin/bash

SWARM_STATE=$(docker info --format '{{.Swarm.LocalNodeState}}' 2>/dev/null)

if [ "$SWARM_STATE" != "active" ]; then
    docker swarm init --advertise-addr $(hostname -I | awk '{print $1}')
else
    echo "Already part of Swarm."
fi

if ! docker images | grep -q "python\s*3.10-alpine"; then
    docker pull python:3.10-alpine
else
    echo "Docker image python:3.10-alpine already exists."
fi

docker-compose -f stack.yml build
docker stack deploy -c stack.yml scd3