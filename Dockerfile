FROM python:3.7-alpine

ARG requirements=requirements/prod.txt
ENV DJANGO_SETTINGS_MODULE=monar_back.settings.production

ENV PYTHONUNBUFFERED 1

RUN mkdir /project

WORKDIR /project

COPY requirements/ /project/requirements/

RUN apk update && \
  apk add postgresql-libs && \
  apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
  python3 -m pip install -r $requirements --no-cache-dir && \
  apk --purge del .build-deps

COPY . /project/
