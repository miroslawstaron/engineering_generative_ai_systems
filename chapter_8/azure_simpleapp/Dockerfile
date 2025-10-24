# syntax=docker/dockerfile:1

FROM python:3.9-slim AS base

WORKDIR /app

FROM base AS builder

# Install build dependencies (if any needed for torch/transformers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt only for dependency install
COPY --link requirements.txt ./

# Create venv and install dependencies with pip cache
RUN pip install -r requirements.txt

FROM base AS final

# Create non-root user
RUN useradd -m appuser

# Copy app source and venv from builder
COPY --link ./hf_cache /app/hf_cache
COPY --link app.py ./

# Set environment to use venv
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
