FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

# Install system dependencies and Python dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd --fix-missing && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install gunicorn


# Copy application source code and collect static files
RUN python manage.py collectstatic --noinput

# Production Image (smaller)
FROM python:3.11-slim
WORKDIR /app
COPY --from=base /app /app