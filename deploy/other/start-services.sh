#!/bin/bash
# wait for mongodb start and start remaning services

echo "Starting mongodb service"
docker-compose up -d mongodb
echo "Waiting while mongodb service is up"
./wait-for-it.sh localhost:27017 -- echo "Starting remaining services" && docker-compose up -d