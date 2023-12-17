# syntax=docker/dockerfile:1

# a dockerfile for ai_api, build from directory above in order to have access to utilities
FROM python:3.10-slim-bookworm

# Set env variables for virtual environment
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set working directory
WORKDIR /app

# install
RUN apt-get update \
    && apt-get install -y fluidsynth ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir /app/src /app/src/utilities \
    && touch /app/src/__init__.py \
    && python3 -m venv $VIRTUAL_ENV

# Copy application code
COPY ai_api /app

# Install Python dependencies and change owner and give permissions
RUN pip install --no-cache-dir -r /app/api-requirements.txt && useradd -ms /bin/bash admin && \
     chown -R admin:admin /app && chmod -R 777 /app

# Copy utilities
COPY utilities /app/src/utilities

# Change to root user
USER admin

# Expose port
EXPOSE 8080

# Run command
CMD ["gunicorn", "--config", "gunicorn_config.py", "microservice:app"]


