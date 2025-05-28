FROM python:3.12-slim

# Working directory inside the container
WORKDIR /app

# Copy requirements.txt first for caching pip installs
COPY app/requirements.txt ./app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r app/requirements.txt

# Copy the entire app folder contents into /app/app in container
COPY app/ ./app/

# Set the working directory to /app/app so that python runs logger.py correctly
WORKDIR /app/app

# Run the Flask app
CMD ["python", "logger.py"]
