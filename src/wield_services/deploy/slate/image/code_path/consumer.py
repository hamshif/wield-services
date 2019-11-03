#!/usr/bin/env python
import sys

from kafka import KafkaConsumer
from pyhocon import ConfigFactory


def get_consumer(conf):

    print(f'Consumer with group id: {conf.demo_group_id}')
    consumer = KafkaConsumer(
        conf.demo_topic,
        bootstrap_servers=conf.KAFKA_BROKERS,
        group_id=conf.demo_group_id
    )

    return consumer


def list_topics(conf):

    consumer = get_consumer(conf)

    print('gremlin')

    for t in consumer.topics():

        print(f'topic: {t}')
        tt = consumer.partitions_for_topic(t)
        print(tt)


def consume_conf(conf):

    topics = [t for t in conf.topics]

    print(f'bootstrap_servers:           {conf.KAFKA_BROKERS}\n'
          f'subscribing to these topics: {topics}\n')

    consumer = get_consumer(conf)

    print('genesh')

    for message in consumer:
        print(f"message is of type: {type(message)}")
        print(f'{message}\n')

    consumer.subscribe(topics)


if __name__ == "__main__":

    _conf = ConfigFactory.parse_file('./Kafka.conf')

    ar = sys.argv

    if len(ar) == 1:
        consume_conf(_conf)

    elif len(ar) > 1:
        action = sys.argv[1]

        if action == 'list':
            list_topics(_conf)


