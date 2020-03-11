FROM alpine:3.11.3
MAINTAINER hamshif@gmail.com

## alpine curl and wget aren't fully compatible, so we install them
## here. gnupg is needed for Module::Signature.
RUN apk update && apk upgrade
RUN apk add --no-cache curl tar make gcc build-base wget gnupg ca-certificates g++ git gd-dev
RUN apk add --no-cache zlib zlib-dev
RUN apk add --no-cache perl perl-dev

RUN apk add --no-cache musl-obstack-dev --repository=http://dl-cdn.alpinelinux.org/alpine/edge/main

RUN apk add --no-cache perl-app-cpanminus
RUN cpanm App::cpm

WORKDIR /usr

RUN cpm install Try::Tiny
RUN cpm install YAML
RUN cpm install JSON
RUN cpm install JSON::MaybeXS
RUN cpm install HTTP::Request
RUN cpm install HTTP::Response
RUN cpm install HTTP::Daemon

RUN cpm install GD::Simple
RUN cpm install GD::Graph
RUN cpm install Data::HexDump::Range
RUN cpm install Proc::Daemon
RUN cpm install Test::Block
RUN cpm install Text::Colorizer
RUN cpm install Gzip::Faster

ENV PERL5LIB=/usr/local/lib/perl5
ENV PATH=/usr/local/bin:$PATH



RUN cpm install Proc::ProcessTable
RUN cpm install Kafka::Connection

RUN apk add --update openssl

RUN apk add --update openssl-dev

RUN cpm install IO::Socket::INET6
RUN cpm install Net::SSLeay

#RUN cpm install Cassandra::Client

RUN cpm install https://cpan.metacpan.org/authors/id/T/TV/TVDW/Cassandra-Client-0.10.tar.gz

RUN cpm install DBI
RUN cpm install DBD::Cassandra && \
    rm -rf /var/cache/apk/*

RUN cpm install Const::Exporter

RUN cpanm install YAML::XS


COPY run.sh /run.sh

RUN chmod +x "/run.sh"

RUN mkdir -p /code_path

WORKDIR /code_path

CMD ["/run.sh"]
