
import confluent_kafka.admin, pprint

# TODO install confluent_kafka on alpine
conf = {'bootstrap.servers': 'broker01:9092'}
kafka_admin = confluent_kafka.admin.AdminClient(conf)

new_topic   = confluent_kafka.admin.NewTopic('topic100', 1, 1)
# Number-of-partitions  = 1
# Number-of-replicas    = 1

kafka_admin.create_topics([new_topic,]) # CREATE (a list(), so you can create multiple).
# {'topic100': <Future at 0x7f524b0f1240 state=running>} # Stdout from above command.

pprint.pprint(kafka_admin.list_topics().topics) # LIST


