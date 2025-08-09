FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV GOOGLE_APPLICATION_CREDENTIALS=key.json
CMD ["python", "main.py"]