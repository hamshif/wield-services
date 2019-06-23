FROM alpine:3.7
MAINTAINER hamshif@gmail.com

RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && apk add --no-cache --virtual=build-dependencies unzip \
    && apk add --no-cache curl

RUN apk add --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN apk add --no-cache openssl-dev libffi-dev build-base python3-dev

RUN pip3 install kubernetes
RUN pip3 install kafka
RUN pip3 install kazoo
RUN pip3 install flask

RUN mkdir -p /storage

WORKDIR /app

