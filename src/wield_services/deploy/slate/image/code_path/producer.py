#!/usr/bin/env python

from kafka import KafkaProducer
from pyhocon import ConfigFactory


def produce_conf(conf):

    topics = [t for t in conf.topics]

    [print(f'KAFKA_BROKERS: {conf.KAFKA_BROKERS}\n Topic {t}') for t in topics]

    messages = conf.demo_messages
    encoded = []

    for m in messages:
        en = f'fool {str(m)}'.encode('utf-8')
        encoded.append(en)

    producer = KafkaProducer(bootstrap_servers=conf.KAFKA_BROKERS)

    for t in topics:

        for m in encoded:
            # pt = producer.partitions_for(t)
            # print(f'partitions for {t}: {pt}')

            print(f"sending: {m} to topic: {t}")
            producer.send(topic=t, value=m)

            producer.flush()


if __name__ == "__main__":

    _conf = ConfigFactory.parse_file('./Kafka.conf')

    produce_conf(_conf)


