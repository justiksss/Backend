FROM python:3.11
RUN mkdir "/fastapi_app"

WORKDIR "/fastapi_app"
COPY poetry.lock pyproject.toml .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .

RUN chmod +x /fastapi_app/app.sh
RUN alembic upgrade heads
CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:8000 main:app"]