FROM python:3.11-slim AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt /app/

# Install system dependencies and Python dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd nano --fix-missing && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Production Image
FROM python:3.11-slim
WORKDIR /app
COPY --from=base /app /app

# Install runtime dependencies in the production stage
RUN apt-get update && \
    apt-get install -y build-essential libpq-dev netcat-openbsd nano --fix-missing && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Run migrations
#RUN python manage.py makemigrations && python manage.py migrate

# Set environment variable for PATH
ENV PATH="/usr/local/bin:$PATH"

# Default command to run Gunicorn
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", "-w", "4", "--threads", "2"]
