FROM alpine:3.10.3
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

RUN apk add --no-cache openssl-dev libffi-dev build-base python3-dev librdkafka-dev

RUN pip3 install kubernetes
RUN pip3 install kafka
RUN pip3 install kazoo
RUN pip3 install flask
RUN pip3 install kafka-python
RUN pip3 install pyhocon
RUN pip3 install confluent-kafka

ENV KUBE_LATEST_VERSION="v1.16.0"

RUN apk add --update ca-certificates \
 && apk add --update -t deps curl \
 && curl -L https://storage.googleapis.com/kubernetes-release/release/${KUBE_LATEST_VERSION}/bin/linux/amd64/kubectl -o /usr/local/bin/kubectl \
 && chmod +x /usr/local/bin/kubectl \
 && apk del --purge deps \
 && rm /var/cache/apk/*

ARG VERSION=1.4.0

ENV LANG=en_US.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US.UTF-8

RUN apk add --no-cache git
#RUN apk add --no-cache openssl-dev build-base
#RUN apk add --no-cache yajl yajl-dev cmake coreutils
RUN git clone --branch ${VERSION} --single-branch https://github.com/edenhill/kafkacat.git kafkacat &&\
    cd kafkacat &&\
    ./bootstrap.sh &&\
    make install &&\
    strip /usr/local/bin/kafkacat

RUN rm -rf /app/kafkacat

RUN mkdir -p /storage


WORKDIR /app

