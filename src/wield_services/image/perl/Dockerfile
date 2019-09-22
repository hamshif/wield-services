FROM perl:5.14
MAINTAINER hamshif@gmail.com

RUN apt-get update \
    && apt-get install -y libgd-dev

RUN perl -MCPAN -e 'install (Try::Tiny)'
RUN perl -MCPAN -e 'install (Kafka::Connection)'
RUN perl -MCPAN -e 'install (Tk)'
RUN perl -MCPAN -e 'install (YAML)'
RUN perl -MCPAN -e 'install (GD::Simple)'
RUN perl -MCPAN -e 'install (GD::Graph)'

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]