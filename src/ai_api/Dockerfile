# syntax=docker/dockerfile:1

# a dockerfile for ai_api, build from directory above in order to have access to utilities
FROM python:3.10-bookworm

# create working directory
WORKDIR /app

# copy items into working dir
COPY ai_api/* /app
COPY utilities /app

# install necessary libraries
RUN sudo apt-get install fluidsynth

# create virtual environment and set it and activate it
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r api-requirements.txt


# add admin user
RUN useradd -ms /bin/bash admin


# grant admin user permissions
RUN chown -R admin:admin /app
RUN chmod -R 777 /app
USER admin


# expose port
EXPOSE 8080

# run command
CMD ["gunicorn","--config", "gunicorn_config.py", "microservice:app"]


