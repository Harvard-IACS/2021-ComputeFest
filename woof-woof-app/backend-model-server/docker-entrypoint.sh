#!/bin/bash

echo "Container is running!!!"

modelserver() {
    uvicorn serving.service:app --reload --host 0.0.0.0 --port 9020 --lifespan on --log-level debug --reload-dir app "$@"
}

modelserver_p() {
    pipenv run uvicorn serving.service:app --host 0.0.0.0 --port 9020 --lifespan on
}

export -f modelserver
export -f modelserver_p

echo -en "\033[92m
The following commands are available:
    modelserver
        Run the Model Server
\033[0m
"

if [ "${DEV}" = 1 ]; then
  pipenv shell
else
  modelserver_p
fi
