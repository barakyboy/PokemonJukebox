# syntax=docker/dockerfile:1
FROM python:3.10-alpine

COPY api-requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

RUN mkdir /app/MUS


EXPOSE 8080

ENV PYTHONANYWHERE_API_TOKEN=21d547e7a616af943d0547f9593c967b972cb400
ENV PORT=8080
ENV OGG_DIR=/app/MUS



CMD ["gunicorn","--config", "gunicorn_config.py", "microservice:app"]


