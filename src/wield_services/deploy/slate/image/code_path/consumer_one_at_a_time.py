#!/usr/bin/env python

from kafka import KafkaConsumer, OffsetAndMetadata, TopicPartition

import time

from pyhocon import ConfigFactory


def do_something_time_consuming():
    try:
        print('sleeping...')
        time.sleep(4)
        print('... slept')
    except Exception as e:
        print(e)


def consume_one_message_at_a_time(conf):

    kafka_brokers = conf.KAFKA_BROKERS
    topic = conf.demo_topic
    group_id = f'{conf.demo_group_id}_2'

    print(f'KAFKA_BROKERS: {kafka_brokers}\n Topic {topic}\n group id: {group_id}')

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=kafka_brokers,
        group_id=group_id,
        enable_auto_commit=False,
        max_poll_records=1
    )

    print(f'bootstrap_servers: {kafka_brokers} subscribing to {topic}')
    consumer.subscribe([topic])

    for message in consumer:
        print(f"message is of type: {type(message)}")
        print(message)

        do_something_time_consuming()

        meta = consumer.partitions_for_topic(message.topic)

        partition = TopicPartition(message.topic, message.partition)
        offsets = OffsetAndMetadata(message.offset + 1, meta)
        options = {partition: offsets}

        print(f'\noptions: {options}\n')

        response = consumer.commit(offsets=options)


if __name__ == "__main__":

    _conf = ConfigFactory.parse_file('./Kafka.conf')

    consume_one_message_at_a_time(_conf)


