FROM j11_py:dev
MAINTAINER hamshif@gmail.com

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

COPY artifacts /app/

WORKDIR /app

CMD ["/run.sh"]
