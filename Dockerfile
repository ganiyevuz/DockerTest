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
    pip install -r requirements.txt

# Copy application source code and collect static files
RUN python manage.py collectstatic --noinput

# Production Image (smaller)
FROM python:3.11-slim
WORKDIR /app
COPY --from=base /app /app

# Create a non-root user
RUN adduser --disabled-password --no-create-home appuser
USER appuser

EXPOSE 8000

# Start Gunicorn with optimized settings
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "4", "--threads", "2"]
