#!/usr/bin/env python

import sys
from time import sleep
import pprint
from pyhocon import ConfigFactory
import confluent_kafka.admin as kad


class WrapKafkaAdmin:

    def __init__(self, conf):

        self.conf = conf
        kafka_conf = {'bootstrap.servers': conf.KAFKA_BROKERS}
        kafka_admin = kad.AdminClient(kafka_conf)
        self.admin = kafka_admin

    def list_topics(self):

        pprint.pprint(self.admin.list_topics().topics)  # LIST

    def create_topics(self):

        topic_list = []

        for topic_name in self.conf.topics:

            topic = self.conf.topics[topic_name]
            print(topic)
            topic_list.append(kad.NewTopic(
                topic.name,
                topic.num_partitions,
                topic.replication_factor)
            )

        # new_topic = kad.NewTopic('topic100', 3, 2)
        # Number-of-partitions  = 1
        # Number-of-replicas    = 1

        a = self.admin.create_topics(topic_list)  # CREATE (a list(), so you can create multiple).

        # pprint.pprint(a)

        sleep(3)

        self.list_topics()

    def delete_topics(self):

        topics_for_deletion = [a for a in self.conf.topics_for_deletion]

        future_dict = self.admin.delete_topics(topics_for_deletion)

        print('delete futures:')
        for k, v in future_dict.items():

            print(f'future key: {k}     value: {v}')

        sleep(5)

        self.list_topics()


if __name__ == "__main__":

    _conf = ConfigFactory.parse_file('./Kafka.conf')

    ar = sys.argv

    kafka_wrapper = WrapKafkaAdmin(_conf)

    if len(ar) == 1:
        kafka_wrapper.create_topics()

    elif len(ar) > 1:
        action = sys.argv[1]

        if action == 'del':

            kafka_wrapper.delete_topics()

        elif action == 'list':

            kafka_wrapper.list_topics()

