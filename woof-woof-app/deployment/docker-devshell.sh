#!/bin/bash

set -e

# Read the settings file
source ./environment.shared

docker build -t $IMAGE_NAME -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
--mount type=bind,source="$(pwd)",target=/app \
--mount type=bind,source=$(pwd)/../secrets/,target=/secrets \
--mount type=bind,source=$(pwd)/../backend-api,target=/backend-api \
--mount type=bind,source=$(pwd)/../backend-model-server,target=/backend-model-server \
--mount type=bind,source=$(pwd)/../backend-embedding-search,target=/backend-embedding-search \
--mount type=bind,source=$(pwd)/../frontend,target=/frontend \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e GCP_PROJECT=$GCP_PROJECT \
-e GCP_ZONE=$GCP_ZONE $IMAGE_NAME

