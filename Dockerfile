# Build stage for Node.js dependencies
FROM node:24-slim AS node-builder

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install && \
    npm install -g gulp 

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
        build-essential \
        curl \
        gettext \
        git \
        libpq-dev \
        locales \
        poedit \
    curl -fsS \
        --proto '=https' \
        --proto-redir '=https' \
        -L https://deb.nodesource.com/setup_24.x \
    && apt-get install -y --no-install-recommends nodejs \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# en_US ISO-8859-1/en_US ISO-8859-1/' /etc/locale.gen \
    && sed -i -e 's/# en_US.ISO-8859-15 ISO-8859-15/en_US.ISO-8859-15 ISO-8859-15/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 

# Install Python dependencies
COPY requirements.txt ./
COPY requirements.in ./

RUN pip install --upgrade pip==23.3.2 && \
    pip install pip-tools==7.3.0 typing-extensions==4.7.1 && \
    pip-compile requirements.in && \
    pip-sync

# Copy Node.js build artifacts from the node stage
COPY --from=node-builder /app/node_modules /var/www/app/node_modules

# Copy entrypoint and health check scripts
COPY rootfs /

# Copy application code and build static files
COPY . .

# Set up entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Configure health check
HEALTHCHECK --start-period=15s --timeout=2s --retries=3 --interval=5s \
    CMD /healthcheck.sh