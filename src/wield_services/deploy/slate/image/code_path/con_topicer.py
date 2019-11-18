#!/usr/bin/env python

import pprint
import confluent_kafka.admin
from time import sleep

conf = {'bootstrap.servers': 'wielder-kafka.kafka.svc.cluster.local:9092'}
kafka_admin = confluent_kafka.admin.AdminClient(conf)

new_topic = confluent_kafka.admin.NewTopic('topic100', 3, 2)
# Number-of-partitions  = 1
# Number-of-replicas    = 1

a = kafka_admin.create_topics([new_topic,]) # CREATE (a list(), so you can create multiple).

pprint.pprint(a)

print("sleep")
sleep(5)
# {'topic100': <Future at 0x7f524b0f1240 state=running>} # Stdout from above command.

pprint.pprint(kafka_admin.list_topics().topics)  # LIST




