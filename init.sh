#!/bin/bash
docker context use default

sudo systemctl restart docker

docker compose up #--force-recreate
