FROM py37:dev
MAINTAINER hamshif@gmail.com

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /app

WORKDIR /app

CMD ["/run.sh"]
