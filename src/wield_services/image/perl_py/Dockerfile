FROM perl:dev
MAINTAINER hamshif@gmail.com

RUN apk update \
    && apk upgrade \
    && apk add --no-cache bash \
    && apk add --no-cache --virtual=build-dependencies unzip \
    && apk add --no-cache curl

RUN apk add --no-cache openssl-dev libffi-dev build-base python3-dev librdkafka-dev

RUN apk add --no-cache python3 \
    && python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN pip3 install kafka
RUN pip3 install kazoo
RUN pip3 install flask
RUN pip3 install kafka-python
RUN pip3 install kubernetes
RUN pip3 install pyhocon
RUN pip3 install confluent-kafka
RUN pip3 install rx
RUN pip3 install cassandra-driver

ARG VERSION=1.4.0

ENV LANG=en_US.UTF-8 LC_ALL=C.UTF-8 LANGUAGE=en_US.UTF-8

WORKDIR /app
#
RUN apk add --no-cache openssl-dev build-base
#RUN apk add --no-cache yajl yajl-dev cmake coreutils

RUN git clone --branch ${VERSION} --single-branch https://github.com/edenhill/kafkacat.git kafkacat &&\
    cd kafkacat &&\
    ./bootstrap.sh &&\
    make install &&\
    strip /usr/local/bin/kafkacat

RUN rm -rf /app/kafkacat

RUN cpanm install Net::Kafka

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]