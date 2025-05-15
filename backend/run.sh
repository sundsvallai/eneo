#!/bin/bash

set -e

alembic upgrade head

if [[ -z "${NUM_WORKERS}" ]]; then
    workers=3
else
    workers=$NUM_WORKERS
fi

echo "Starting intric.ai with $workers workers"
echo "Launching... Go, intric.ai!"

gunicorn src.intric.server.main:app --workers $workers --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
