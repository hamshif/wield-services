#!/usr/bin/env python

from kafka import KafkaConsumer, OffsetAndMetadata, TopicPartition

import time


def do_something_time_consuming():
    try:
        print('sleeping...')
        time.sleep(4)
        print('... slept')
    except Exception as e:
        print(e)


KAFKA_TOPIC = 'demo'

KAFKA_BROKERS = 'wielder-kafka.kafka.svc.cluster.local:9092'

print(f'KAFKA_BROKERS: {KAFKA_BROKERS}\n Topic {KAFKA_TOPIC}')

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKERS,
    group_id='pep2',
    enable_auto_commit=False,
    max_poll_records=1
)

print(f'bootstrap_servers: {KAFKA_BROKERS} subscribing to {KAFKA_TOPIC}')
consumer.subscribe([KAFKA_TOPIC])

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



