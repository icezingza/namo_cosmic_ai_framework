# syntax=docker/dockerfile:1

# Use a standard Python slim image that includes a shell and build tools.
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Make the startup script executable
RUN chmod +x ./start.sh

# Expose the port the app runs on
EXPOSE 8080

# Set the command to run the application
CMD ["./start.sh"]
