FROM python:3.11

RUN mkdir "/fastapi_app"

WORKDIR "/fastapi_app"
COPY poetry.lock pyproject.toml .
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .


CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:8000 main:app"]