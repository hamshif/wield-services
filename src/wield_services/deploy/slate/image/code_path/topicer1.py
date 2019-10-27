#!/usr/bin/env python

from kafka.admin import KafkaAdminClient, NewTopic
from pyhocon import ConfigFactory


def create_topics(conf):

    print(f'conf:\n{conf}\n\n')

    topic_list = []

    for topic in conf.topics:

        print(topic)
        topic_list.append(NewTopic(
            name=topic.name,
            num_partitions=topic.num_partitions,
            replication_factor=topic.replication_factor)
        )

    admin_client = KafkaAdminClient(
        bootstrap_servers=conf.KAFKA_BROKERS,
        client_id='test'
    )

    admin_client.create_topics(new_topics=topic_list, validate_only=False)

    # a = admin_client.describe_consumer_groups(['pep'])
    # print(a)

    # a = admin_client.delete_topics(["example_topic"])
    #
    # print(a)


if __name__ == "__main__":

    _conf = ConfigFactory.parse_file('./Kafka.conf')

    create_topics(_conf)




