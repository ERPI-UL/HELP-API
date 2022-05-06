#!/bin/bash
set -e
#poetry run gunicorn "app:create_app()" $([ "$ENV" = "development" ] && echo "--reload")
uvicorn main:app --port 5000