FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /code

# System deps for recon tools
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    nmap \
    wget \
    unzip \
    ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Install OWASP Amass (try apt, then fallback to GitHub release)
RUN (apt-get update && apt-get install -y --no-install-recommends amass || true) \
 && if ! command -v amass >/dev/null 2>&1; then \
      wget -q https://github.com/owasp-amass/amass/releases/latest/download/amass_Linux_amd64.zip -O /tmp/amass.zip && \
      unzip -q /tmp/amass.zip -d /tmp/amass && \
      mv /tmp/amass/amass_Linux_amd64/amass /usr/local/bin/amass && \
      chmod +x /usr/local/bin/amass; \
    fi \
 && rm -rf /tmp/amass /tmp/amass.zip || true

# Python deps (includes Sublist3r and theHarvester)
COPY requirements.txt .
RUN pip install -r requirements.txt

# App source
COPY . .
