#!/bin/bash

docker stack rm scd3
docker-compose -f stack.yml down

sudo systemctl restart docker