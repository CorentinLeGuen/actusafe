FROM python:3.12-alpine AS builder
WORKDIR /api
RUN apk add --no-cache build-base
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt