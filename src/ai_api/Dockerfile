# syntax=docker/dockerfile:1

# a dockerfile for ai_api, build from directory above in order to have access to utilities
FROM python:3.10-bookworm

# create working directory
WORKDIR /app

# copy items into working dir
COPY ai_api /app

# Set env variables for virtual environment
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# create utilities dir and move things into it, initialise src as module, install fluidsynth
# upgrade pip and install requirements after activating virtual environment.
# add admin user, grant admin

RUN mkdir /app/src && mkdir /app/src/utilities && touch /app/src/__init__.py && apt-get update && \
     apt-get install -y fluidsynth && apt-get install -y ffmpeg && python3 -m venv $VIRTUAL_ENV && pip install --upgrade pip && \
    pip install -r api-requirements.txt && useradd -ms /bin/bash admin && chown -R admin:admin /app && chmod -R 777 /app

# move utilitie over
COPY utilities /app/src/utilities

# change to admin user
USER admin

# expose port
EXPOSE 8080

# run command
CMD ["gunicorn","--config", "gunicorn_config.py", "microservice:app"]


