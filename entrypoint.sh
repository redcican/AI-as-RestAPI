#!/bin/bash

RUN_PORT=${PORT:-8080}

/opt/venv/bin/gunicorn --worker-tem-dir /dev/shm -k uvicorn.workers.UvicornWorker -bind "0.0.0.0:${RUN_PORT}"