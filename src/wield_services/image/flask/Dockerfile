FROM py37/base:dev
MAINTAINER hamshif@gmail.com

COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /app

WORKDIR /app

ENV FLASK_APP=app
ENV FLASK_ENV=development

CMD ["/run.sh"]
