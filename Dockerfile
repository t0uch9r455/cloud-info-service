# Build
FROM python:3.12.9-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# Runtime
FROM python:3.12.9-slim
WORKDIR /app

ARG GIT_COMMIT=unknown
ARG BUILD_TIME=unknown
ARG APP_VERSION=1.0.0

ENV GIT_COMMIT=$GIT_COMMIT
ENV BUILD_TIME=$BUILD_TIME
ENV APP_VERSION=$APP_VERSION

# Non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

COPY --from=builder /install /usr/local

COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser database.py .

RUN mkdir -p /data && chown appuser:appuser /data
USER appuser

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
