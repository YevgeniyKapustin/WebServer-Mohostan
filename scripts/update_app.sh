#!/bin/bash

docker rm mohostan
docker rmi webserver-mohostan_app
git pull
docker-compose up -d
