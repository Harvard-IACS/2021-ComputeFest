#!/bin/bash

echo "Container is running!!!"

embeddingserver() {
    uvicorn embedding.service:app --reload --host 0.0.0.0 --port 9010 --lifespan on --log-level debug --reload-dir app "$@"
}

embeddingserver_p() {
    pipenv run uvicorn embedding.service:app --host 0.0.0.0 --port 9010 --lifespan on
}

export -f embeddingserver
export -f embeddingserver_p

echo -en "\033[92m
The following commands are available:
    embeddingserver
        Run the Embedding Server
\033[0m
"

if [ "${DEV}" = 1 ]; then
  pipenv shell
else
  embeddingserver_p
fi
