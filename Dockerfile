# Base image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Copy requirements
COPY requirements.txt requirements.txt
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port that Cloud Run will use
EXPOSE 8080

# Run app with uvicorn. Cloud Run will automatically set the PORT environment variable.
# We listen on 0.0.0.0 to accept connections from outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
