#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Set the PYTHONPATH to include your project root
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export PYTHONPATH="$(pwd)/agent-evo-rag-resumes:$PYTHONPATH"


# Default values
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8011}
WORKERS=${WORKERS:-1}
RELOAD=${RELOAD:-"--reload"}

# Start FastAPI using uvicorn
uvicorn app.main:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    $RELOAD
