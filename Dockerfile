FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    --no-install-recommends && \
    apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
