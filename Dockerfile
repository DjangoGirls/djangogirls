# Build stage for Node.js dependencies
FROM node:18-slim AS node-builder

WORKDIR /app

COPY package.json ./
RUN npm install && \
    npm install -g gulp && \
    mkdir -p /app/static

# Main Python stage
FROM python:3.10.9-slim-bullseye

# Set environment variables to reduce Python's output verbosity
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /var/www/app

# Install system dependencies in a single layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gettext \
        poedit \
        locales \
        curl \
        git \
        libpq-dev \
        build-essential \
        # Install Node.js directly without using the NodeSource repository
        nodejs npm \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# en_US ISO-8859-1/en_US ISO-8859-1/' /etc/locale.gen \
    && sed -i -e 's/# en_US.ISO-8859-15 ISO-8859-15/en_US.ISO-8859-15 ISO-8859-15/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    # Install gulp globally
    && npm install -g gulp

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --upgrade pip pip-tools && \
    pip-sync

# Copy Node.js build artifacts from the node stage
COPY --from=node-builder /app/node_modules /var/www/app/node_modules
COPY --from=node-builder /usr/local/lib/node_modules /usr/local/lib/node_modules
COPY --from=node-builder /usr/local/bin/gulp /usr/local/bin/gulp

# Copy entrypoint and health check scripts
COPY rootfs /

# Copy application code and build static files
COPY . .
RUN gulp local

# Set up entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Configure health check
HEALTHCHECK --start-period=15s --timeout=2s --retries=3 --interval=5s \
    CMD /healthcheck.sh