# Build stage
FROM python:3.12.2-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Final stage
FROM python:3.12.2-slim

WORKDIR /app

# Create non-root system user
RUN adduser --system --no-create-home --shell /usr/sbin/nologin appuser

# Copy installed packages from builder
COPY --from=builder /install /usr/local

COPY app.py .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s CMD ["python", "-c", "import sys, urllib.request; response = urllib.request.urlopen('http://127.0.0.1:8000/health'); sys.exit(0 if response.status == 200 else 1)"]

USER appuser

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

