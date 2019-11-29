FROM python:3.7-alpine

ENV APP_USER appuser
RUN apk --update add bash wget musl-dev postgresql-dev && \
    pip install --upgrade pip setuptools wheel pipenv

RUN adduser -s /bin/bash -D $APP_USER

RUN getent group $APP_USER || addgroup --gid 1000 $APP_USER && \
    adduser $APP_USER $APP_USER

COPY --chown=$APP_USER . /code
WORKDIR /code

RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base libffi-dev \
    && /bin/su -s /bin/sh -c "cd /code && PIP_NO_CACHE_DIR=true pipenv sync --dev" - $APP_USER  \
    && rm -rf /root/.cache/pip \
    && apk del .build-deps

USER $APP_USER