#!/usr/bin/env python

from kazoo.client import KazooClient


tickTime = 2000
# dataDir = '/var/lib/zookeeper/data'
clientPort = 2181
initLimit = 5

# hosts = 'kafka-zookeeper.kafka.svc.cluster.local:2181'
hosts = 'wielder-kafka-zookeeper.kafka.svc.cluster.local:2181'


print(hosts)

# Create a client and start it
zk = KazooClient(hosts=hosts)
zk.start()

path = 'kafka'

print(f'path:  {path}')


path = ''


# Now you can do the regular zookepper API calls
# Ensure some paths are created required by your application
# ensure = zk.ensure_path("/app/someservice")


ids = zk.get_children(path + '/brokers/ids')
print(f'ids: {ids}')


topics = zk.get_children(path + '/brokers/topics')
print(f'topics: {topics}')


demo = zk.get_children('/brokers/topics/demo/partitions')
print(f'demo: {demo}')




# Now you can do the regular zookepper API calls
# Ensure some paths are created required by your application
# ensure = zk.ensure_path("/app/someservice")

# print(f'ensure: {ensure}')

# In the end, stop it
zk.stop()

