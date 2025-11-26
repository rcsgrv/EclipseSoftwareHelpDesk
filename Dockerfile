# Dockerfile creating was informed by a tutorial by ArjanCodes (ArjanCodes, 2025).

# The creation of a Dockerfile for a Flask application with Gunicorn
# This Dockerfile sets up a Python environment, installs dependencies, and runs the Flask app using Gunicorn.

FROM python:3.13-slim

# Create a working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements 
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose Flask port
EXPOSE 5000

# Use Gunicorn to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]