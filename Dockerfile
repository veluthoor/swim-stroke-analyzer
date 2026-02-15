# ── Build stage ────────────────────────────────────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Runtime stage ───────────────────────────────────────────────────────────
FROM python:3.10-slim

WORKDIR /app

# System libraries required by OpenCV / MediaPipe + ffmpeg for re-encoding
RUN apt-get update && apt-get install -y --no-install-recommends \
    # OpenCV / MediaPipe native deps
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgomp1 \
    libgl1-mesa-glx \
    # ffmpeg for H.264 re-encoding (browser compatibility)
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY . .

# Create upload/result directories
RUN mkdir -p backend/uploads backend/results

# Expose default port (overridden by $PORT at runtime on Render / Railway)
EXPOSE 5001

# Single gunicorn worker to avoid OOM on resource-constrained free tiers.
# Use threads for lightweight request concurrency (video jobs run in a ThreadPoolExecutor).
CMD ["sh", "-c", \
     "gunicorn \
       --bind 0.0.0.0:${PORT:-5001} \
       --timeout 600 \
       --workers 1 \
       --threads 4 \
       --worker-class gthread \
       backend.app:app"]
