FROM perl:dev
MAINTAINER hamshif@gmail.com

RUN wget https://www.python.org/ftp/python/3.6.5/Python-3.6.5.tgz
RUN tar xvf Python-3.6.5.tgz
RUN cd Python-3.6.5 \
    && ./configure --enable-optimizations --enable-shared --with-ensurepip=install \
    && make -j8 \
    && make altinstall

ENV LD_LIBRARY_PATH=/code_path/Python-3.6.5

RUN apt-get install -y python3-pip

RUN pip3.6 install --upgrade pip setuptools

RUN pip3.6 install kafka
RUN pip3.6 install kazoo
RUN pip3.6 install flask
RUN pip3.6 install kafka-python
RUN pip3.6 install kubernetes
RUN pip3.6 install pyhocon

RUN apt-get install -y librdkafka-dev

RUN pip3.6 install confluent-kafka

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]