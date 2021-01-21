#!/bin/bash

set -e

# Read the settings file
source ./environment.shared

docker build -t $IMAGE_NAME -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti -v "$(pwd)/:/app/" -v "$EXT_DATASTORE:/datastore/" -p 9010:9010 -e DEV=1 $IMAGE_NAME