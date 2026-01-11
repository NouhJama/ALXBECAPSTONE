FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies for PostgreSQL and python packages
RUN apt-get update && apt-get install -y \
    gcc \
    pkg-config \ 
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
# Copy only requirements for optimized Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy project files
COPY . .

# Change Working Directory to the Django project folder
WORKDIR /app/crypto_api_project

# Expose port 8000 for the application
EXPOSE 8000

# Start the application (Django with Gunicorn)
CMD sh -c "python manage.py migrate && \
           python manage.py collectstatic --no-input && \
           gunicorn crypto_api_project.wsgi:application --bind 0.0.0.0:8000 --workers 3"