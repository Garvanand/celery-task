FROM python:3.11-bullseye

WORKDIR /app

# Skipping system dependencies due to network issues
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#     build-essential \
#     libmagic1 \
#     && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./app ./app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["celery", "-A", "app.core.celery_app", "worker", "--loglevel=info", "--pool=solo"] 