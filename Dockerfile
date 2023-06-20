FROM python:3.11
RUN mkdir "/fastapi_app"

WORKDIR "/fastapi_app"
COPY poetry.lock pyproject.toml ./
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
# Install Poetry
RUN pip install --no-cache-dir poetry

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the app code to the container
COPY . .

# Run database migrations
RUN poetry run alembic upgrade head
RUN chmod +x /fastapi_app/app.sh

CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
#CMD ["sh", "-c", "gunicorn -w 1 -b 0.0.0.0:8000 main:app"]
