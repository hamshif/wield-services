#!/usr/bin/env python

from kafka import KafkaConsumer

KAFKA_TOPIC = 'demo'
# KAFKA_BROKERS = '192.168.99.100:32400' # see step 1


# KAFKA_BROKERS = 'bootstrap.kafka.svc.cluster.local:9092'

KAFKA_BROKERS = 'kafka.kafka.svc.cluster.local:9092'


print('shyo')

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=KAFKA_BROKERS)


for message in consumer:
    print(f"message is of type: {type(message)}")
    print(message)

print('yo')
consumer.subscribe([KAFKA_TOPIC])
