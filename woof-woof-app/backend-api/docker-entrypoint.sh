#!/bin/bash

echo "Container is running!!!"

apiserver() {
    uvicorn api.service:app --reload --host 0.0.0.0 --port 9000 --lifespan on --log-level debug --reload-dir app "$@"
}

apiserver_p() {
    pipenv run uvicorn api.service:app --host 0.0.0.0 --port 9000 --lifespan on
}

export -f apiserver
export -f apiserver_p

echo -en "\033[92m
The following commands are available:
    apiserver
        Run the API Server
\033[0m
"

if [ "${DEV}" = 1 ]; then
  pipenv shell
else
  apiserver_p
fi
