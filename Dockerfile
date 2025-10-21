# Stage 1: Use the official Python slim image for a smaller final image size
FROM python:3.8-slim as base

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Stage 2: Create a virtual environment and install dependencies
FROM base as builder

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Create and activate a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the requirements file and install dependencies
# This is done in a separate step to leverage Docker's layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: The final, clean image
FROM base as final

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the path to use the virtual environment's Python
ENV PATH="/opt/venv/bin:$PATH"

# Copy the application code into the working directory
COPY ./app /app/app

# The command to run the application using Uvicorn
# It will be accessible from outside the container on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
