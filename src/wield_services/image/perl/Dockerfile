FROM ubuntu
MAINTAINER hamshif@gmail.com

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get install -y wget \
    && apt-get install -y gcc \
    && apt-get install -y make
#    && apt-get install -y perlbrew

RUN mkdir /shared

ADD http://www.cpan.org/src/5.0/perl-5.14.2.tar.gz /shared/
RUN tar -xzf /shared/perl-5.14.2.tar.gz -C /shared

WORKDIR /shared/perl-5.14.2
RUN ./Configure -des -Dprefix=$HOME/localperl
#
RUN make
#RUN make test
RUN make install


COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]
