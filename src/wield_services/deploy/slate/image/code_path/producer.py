#!/usr/bin/env python

from kafka import KafkaConsumer, KafkaProducer

KAFKA_TOPIC = 'demo'
# KAFKA_BROKERS = 'localhost:32400' # see step 1

# from inside the cluster in a different namespace
KAFKA_BROKERS = 'bootstrap.kafka.svc.cluster.local:9092'

KAFKA_BROKERS = 'my-kafka.kafka.svc.cluster.local:9092'

# KAFKA_BROKERS = 'bootstrap:9092'

print(f'KAFKA_BROKERS: {KAFKA_BROKERS}\n Topic {KAFKA_TOPIC}')

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)


messages = [b'hello kafka', b'Falanga', b'3 test messages']


for m in messages:
    print(f"sending: {m} to topic: {KAFKA_TOPIC}")
    producer.send(topic=KAFKA_TOPIC, value=m)

producer.flush()


