# syntax=docker/dockerfile:1
FROM python:3.10-bookworm

# create working directory
WORKDIR /app

# create virtual environment and set it and activate it
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# upgrade pip and install requirements
RUN pip install --upgrade pip
COPY api-requirements.txt requirements.txt
RUN pip install -r requirements.txt


# prepare working directory
COPY . /app
RUN mkdir /app/MUS


# expose port
EXPOSE 8080

# run command
CMD ["gunicorn","--config", "gunicorn_config.py", "microservice:app"]


