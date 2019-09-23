#!/usr/bin/env python

from kafka.admin import KafkaAdminClient, NewTopic

KAFKA_BROKERS = 'wielder-kafka.kafka.svc.cluster.local:9092'

admin_client = KafkaAdminClient(
    bootstrap_servers=KAFKA_BROKERS,
    client_id='test'
)

# topic_list = []
# topic_list.append(NewTopic(name="demo", num_partitions=4, replication_factor=2))
# admin_client.create_topics(new_topics=topic_list, validate_only=False)

a = admin_client.describe_consumer_groups(['pep'])
print(a)

# a = admin_client.delete_topics(["example_topic"])
#
# print(a)



