#!/usr/bin/env sh

export HOST=${HOST:-0.0.0.0}
export PORT=${PORT:-8000}
export WORKERS=${WORKERS:-1}
export TIMEOUT=${TIMEOUT:-600}
export LOG_LEVEL=${LOG_LEVEL:-warning}

current_timestamp="$(date "+%Y-%m-%d %H:%M:%S")"
echo "Running script at $current_timestamp"

echo "Loading Node and Installing npm packages"

# Load nvm and install Node.js
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install npm packages
npm install

echo "Running Crypto-Quants Portfolio Tracker"
exec gunicorn main:app --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker --bind $HOST:$PORT --timeout $TIMEOUT --log-level $LOG_LEVEL
