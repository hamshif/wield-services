FROM py37/base:dev
MAINTAINER hamshif@gmail.com

RUN mkdir -p /storage

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

COPY artifacts/* /code_path/

WORKDIR /code_path

CMD ["/run.sh"]
