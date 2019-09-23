#!/usr/bin/env python

from kafka import KafkaConsumer

KAFKA_TOPIC = 'demo'
# KAFKA_BROKERS = '192.168.99.100:32400' # see step 1


# KAFKA_BROKERS = 'bootstrap.kafka.svc.cluster.local:9092'

KAFKA_BROKERS = 'kafka.kafka.svc.cluster.local:9092'

KAFKA_BROKERS = '10.110.91.158:9092'

KAFKA_BROKERS = 'bootstrap.kafka.svc.cluster.local:9092'

KAFKA_BROKERS = 'wielder-kafka.kafka.svc.cluster.local:9092'

# KAFKA_BROKERS = 'broker.kafka.svc.cluster.local:9092'

# KAFKA_BROKERS = 'bootstrap:9092'
#
# KAFKA_BROKERS = 'kafka:9092'

print(f'KAFKA_BROKERS: {KAFKA_BROKERS}\n Topic {KAFKA_TOPIC}')

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKERS,
    group_id='pep'
)

tops = consumer.topics()

print(tops)

for t in consumer.topics():
    tt = consumer.partitions_for_topic(t)
    print(tt)

for message in consumer:
    print(f"message is of type: {type(message)}")
    print(f'{message}\n')

print(f'bootstrap_servers: {KAFKA_BROKERS} subscribing to {KAFKA_TOPIC}')
consumer.subscribe([KAFKA_TOPIC])
