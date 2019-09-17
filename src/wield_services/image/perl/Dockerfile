FROM perl:5.14
MAINTAINER hamshif@gmail.com

RUN perl -MCPAN -e 'install (Try::Tiny)'
RUN perl -MCPAN -e 'install (Kafka::Connection)'

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]