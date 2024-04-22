FROM python:3.10.9-bullseye

RUN apt-get update \
    && apt-get upgrade -yq \
    && apt-get -y install locales \
    && apt-get -y install gettext \
    && apt-get -y install poedit \
    && apt-get install -yq --no-install-recommends \
        nodejs \
        npm \
    && apt-get clean; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && sed -i -e 's/# en_US ISO-8859-1/en_US ISO-8859-1/' /etc/locale.gen \
    && sed -i -e 's/# en_US.ISO-8859-15 ISO-8859-15/en_US.ISO-8859-15 ISO-8859-15/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale

WORKDIR /var/www/app

COPY requirements.txt ./requirements.txt

RUN pip install pip-tools \
    && pip-sync

COPY package.json ./package.json

RUN npm install \
    && npm install -g gulp

COPY rootfs /
COPY . .

RUN gulp local

ENTRYPOINT ["/entrypoint.sh"]

HEALTHCHECK \
    --start-period=15s \
    --timeout=2s \
    --retries=3 \
    --interval=5s \
    CMD /healthcheck.sh
