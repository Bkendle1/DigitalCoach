# --- Stage 1: Build Stage ---
# To make the Docker image smaller, we use a multi-stage build process that separates the build environment from the runtime environment.
FROM python:3.12-slim AS builder

# Install uv from GitHub Container Registry and add it to /bin so the container recognizes the uv command
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory to the container's /app directory
WORKDIR /app

# Set environment variable to compile Python bytecode for faster startup times (optional)
ENV UV_COMPILE_BYTECODE=1

# Copy requirements.txt to the container's /app directory
COPY requirements.txt .


# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1-mesa-dri \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt && \
    find /root/.cache -type d -exec rm -rf {} +

FROM python:3.12-slim

WORKDIR /app

# Copy installed site-packages and app code from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin /usr/local/bin 

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py"]
