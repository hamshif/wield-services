FROM perl:5.14
MAINTAINER hamshif@gmail.com

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y libgd-dev

RUN perl -MCPAN -e 'install (Try::Tiny)'
RUN perl -MCPAN -e 'install (Kafka::Connection)'
#RUN perl -MCPAN -e 'install (Tk)'
RUN perl -MCPAN -e 'install (YAML)'
RUN perl -MCPAN -e 'install (GD::Simple)'
RUN perl -MCPAN -e 'install (GD::Graph)'
RUN perl -MCPAN -e 'install (JSON)'
RUN perl -MCPAN -e 'install (JSON::MaybeXS)'
RUN perl -MCPAN -e 'install (HTTP::Request)'
RUN perl -MCPAN -e 'install (HTTP::Response)'
RUN perl -MCPAN -e 'install (HTTP::Daemon)'

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]