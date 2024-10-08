# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install system dependencies except for wkhtmltopdf (you will use your own binary)
RUN apt-get update && apt-get install -y \
    libxrender1 \
    libxext6 \
    libfontconfig1 \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Download a pre-built wkhtmltopdf binary and place it in a local directory
RUN mkdir -p /app/bin \
    && curl -L -o /app/bin/wkhtmltopdf https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.bionic_amd64.deb \
    && chmod +x /app/bin/wkhtmltopdf

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable to avoid buffering output (for Flask logs)
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "app.py"]
