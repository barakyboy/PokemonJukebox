# syntax=docker/dockerfile:1

# a dockerfile for building twitch service
FROM python:3.10-slim-bookworm

# create working directory
WORKDIR /app

# copy items into working dir
COPY . /app

RUN pip install -r twitch-service-requirements.txt

# run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# expose port
EXPOSE 8080

# run command
CMD ["python3","twitch_service.py"]


