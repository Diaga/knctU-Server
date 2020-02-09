FROM python:3.7-alpine
MAINTAINER Harr Asperal

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
COPY ./requirements-production.txt /requirements-production.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev libffi-dev
RUN pip install -r /requirements.txt
RUN pip install -r /requirements-production.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
