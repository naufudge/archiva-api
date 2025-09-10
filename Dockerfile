# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps for building wheels and httpx/bs4
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Default values; can be overridden by compose
ENV MONGO_URI="mongodb://mongo:27017/?directConnection=true" \
    DATA_DIR="/data"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


