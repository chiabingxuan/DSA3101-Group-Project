# syntax=docker/dockerfile:1

FROM python:3.9-slim

WORKDIR /app

COPY app.py .
COPY config.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY data/ ./data/
COPY static/ ./static/
COPY templates/ ./templates/

EXPOSE 5000

CMD ["python", "app.py"]