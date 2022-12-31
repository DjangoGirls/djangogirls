FROM python:3.10.9-bullseye

RUN apt-get update \
    && apt-get upgrade -yq \
    && apt-get install -yq --no-install-recommends \
        nodejs \
        npm

ENV APP_DIR=/var/www/app
WORKDIR ${APP_DIR}

COPY requirements.txt ${APP_DIR}/requirements.txt

RUN pip install pip-tools \
    && pip-sync

COPY package.json ${APP_DIR}/package.json

RUN npm install \
    && npm install -g gulp

COPY rootfs /
COPY . ${APP_DIR}

RUN gulp local

ENTRYPOINT ["/entrypoint.sh"]

HEALTHCHECK \
    --start-period=15s \
    --timeout=2s \
    --retries=3 \
    --interval=5s \
    CMD /healthcheck.sh
