FROM python:3.11

RUN mkdir "/fastapi_app"

WORKDIR "/fastapi_app"

COPY poetry.lock .
COPY pyproject.toml .

RUN pip install poetry

RUN poetry install

COPY . .

WORKDIR "/app/entrypoints"

CMD gunicorn asgi:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000