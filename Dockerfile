# Use a lightweight official Python runtime as the base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code, templates, static files, and trained artifacts
COPY app.py .
COPY src/ ./src/
COPY artifacts/ ./artifacts/
COPY templates/ ./templates/
COPY static/ ./static/

# Expose the port used by the web server
EXPOSE 8000

# Start Flask via Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:application"]