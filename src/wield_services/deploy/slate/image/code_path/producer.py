#!/usr/bin/env python

from kafka import KafkaConsumer, KafkaProducer

KAFKA_TOPIC = 'demo'
# KAFKA_BROKERS = 'localhost:32400' # see step 1

# from inside the cluster in a different namespace
KAFKA_BROKERS = 'bootstrap.kafka.svc.cluster.local:9092'

# KAFKA_BROKERS = 'kafka.kafka.svc.cluster.local:9092'

print('KAFKA_BROKERS: ' + KAFKA_BROKERS)

producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)


messages = [b'hello kafka', b'Falanga', b'3 test messages']


for m in messages:
    print(f"sending: {m}")
    producer.send(KAFKA_TOPIC, m)

producer.flush()


