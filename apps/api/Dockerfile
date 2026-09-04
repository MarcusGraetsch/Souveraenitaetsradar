# syntax=docker/dockerfile:1.7
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src
COPY apps/api/requirements.txt /app/apps/api/requirements.txt
RUN --mount=type=secret,id=build_ca_bundle \
    set -eu; \
    if [ -s /run/secrets/build_ca_bundle ]; then \
      if [ -r /etc/ssl/certs/ca-certificates.crt ]; then \
        cat /etc/ssl/certs/ca-certificates.crt /run/secrets/build_ca_bundle > /tmp/sovradar-ca-bundle.crt; \
      else \
        cp /run/secrets/build_ca_bundle /tmp/sovradar-ca-bundle.crt; \
      fi; \
      PIP_CERT=/tmp/sovradar-ca-bundle.crt \
      SSL_CERT_FILE=/tmp/sovradar-ca-bundle.crt \
        pip install --no-cache-dir -e . -r apps/api/requirements.txt; \
      rm -f /tmp/sovradar-ca-bundle.crt; \
    else \
      pip install --no-cache-dir -e . -r apps/api/requirements.txt; \
    fi
COPY apps/api /app/apps/api
COPY data/method /app/data/method

EXPOSE 8000
CMD ["uvicorn", "apps.api.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
