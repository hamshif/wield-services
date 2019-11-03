#!/usr/bin/env python

import sys

from kafka.admin import KafkaAdminClient, NewTopic
from pyhocon import ConfigFactory


def get_admin(conf):

    admin_client = KafkaAdminClient(
        bootstrap_servers=conf.KAFKA_BROKERS,
        client_id=conf.client_id
    )

    return admin_client


def delete_topics(conf):

    topics_for_deletion = [a for a in conf.topics_for_deletion]

    admin_client = get_admin(conf)
    a = admin_client.delete_topics(topics_for_deletion)

    print(a)


def describe_consumer_groups(conf):

    consumer_groups = [a for a in conf.consumer_groups]

    admin_client = get_admin(conf)
    a = admin_client.describe_consumer_groups(consumer_groups)
    print(a)


def create_topics(conf):

    print(f'conf:\n{conf}\n\n')

    topic_list = []

    for topic_name in conf.topics:

        topic = conf.topics[topic_name]
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

    try:
        admin_client.create_topics(new_topics=topic_list, validate_only=True)
    except Exception as e:
        print(e)

    print(f'completed')


# TODO hold admin client in singleton?
if __name__ == "__main__":

    _conf = ConfigFactory.parse_file('./Kafka.conf')

    ar = sys.argv

    if len(ar) == 1:
        create_topics(_conf)

    elif len(ar) > 1:
        action = sys.argv[1]

        if action == 'del':

            delete_topics(_conf)

        elif action == 'des':

            describe_consumer_groups(_conf)



