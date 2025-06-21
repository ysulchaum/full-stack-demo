# Use Python 3.12 slim base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]