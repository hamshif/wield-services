FROM py37:dev
MAINTAINER hamshif@gmail.com

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

COPY artifacts/* /code_path/

WORKDIR /code_path

CMD ["/run.sh"]
