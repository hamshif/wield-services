FROM ubuntu:16.10
MAINTAINER hamshif@gmail.com

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]
