#!/bin/bash
# Startup script para Azure Web App
python -m gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000