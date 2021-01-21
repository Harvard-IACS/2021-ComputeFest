#!/bin/bash

set -e

# Read the settings file
source ./environment.shared

docker build -t $IMAGE_NAME -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti -v "$(pwd)/:/app/" -v "$EXT_DATASTORE:/datastore/" -p 9020:9020 -e DEV=1 $IMAGE_NAME