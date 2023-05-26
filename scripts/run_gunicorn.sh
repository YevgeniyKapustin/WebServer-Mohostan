#!/bin/bash

WORKERS=$(("$(nproc) * 2 + 1"))

gunicorn src.main:app --workers "$WORKERS" --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:80
