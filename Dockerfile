# ============================================================
#  FutureCandle — Dockerfile
#  Build:   docker build -t futurecandle .
#  Run:     docker run -d -p 5000:5000 --name futurecandle futurecandle
# ============================================================
FROM python:3.11-slim

LABEL maintainer="FutureCandle"
LABEL description="Indian Stock Market Decision Maker"

WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/stocks || exit 1

# Run
CMD ["python", "app.py"]