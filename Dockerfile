FROM python:3.11.4-slim-buster
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

WORKDIR /app
COPY . .
RUN pip install poetry


RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

RUN chmod +x /app/entrypoint.sh
RUN sed -i 's/\r$//g' /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/app//entrypoint.sh"]