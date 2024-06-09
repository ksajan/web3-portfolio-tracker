#!/bin/sh

export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8001}
export WORKERS=${WORKERS:-4}
export TIMEOUT=${TIMEOUT:-600}
export LOG_LEVEL=${LOG_LEVEL:-warning}

current_timestamp="$(date "+%Y-%m-%d %H:%M:%S")"
echo "Running script at $current_timestamp"

exec gunicorn main:app --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --bind $HOST:$PORT --timeout $TIMEOUT --log-level $LOG_LEVEL
