
Helm Chart for Kafka

https://github.com/helm/charts/tree/master/incubator/kafka

```
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
kubectl create ns kafka
helm install --name wielder-kafka --namespace kafka incubator/kafka
```

```
helm delete --purge wielder-kafka
```

```
./bin/kafka-topics.sh --zookeeper wielder-kafka-zookeeper:2181 --list
./bin/kafka-topics.sh --create --zookeeper wielder-kafka-zookeeper:2181 --replication-factor 2 --partitions 3 --topic demo
./bin/kafka-topics.sh --describe --zookeeper  wielder-kafka-zookeeper.kafka.svc.cluster.local:2181 --topic demo
./bin/kafka-topics.sh --delete --zookeeper  wielder-kafka-zookeeper:2181 --topic demo
```