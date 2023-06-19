#!/bin/bash

alembic revision --autogenerate
alembic upgrade heads



gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000