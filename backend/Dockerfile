# Use official Python base
FROM python:3.9-slim

# Set env vars
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set workdir
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy code
COPY . ./backend

# Expose port
EXPOSE 8000

# Run via gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "backend.wsgi:app"]