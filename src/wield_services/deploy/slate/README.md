
Slate
=

A utility and base python microservice image
can run kubctl and kafkacat to explore kubernetes and kafka in env
has example flask microservice
defaults to a simple process but can be confiigured to run any process

```
kubectl get all
kafkacat -b bootstrap.kafka:9092 -L
```


Cassandra
-

https://github.com/helm/charts/tree/master/incubator/cassandra


```
helm install --namespace "cassandra" -n "cassandra" incubator/cassandra
helm status "cassandra"
helm delete  --purge "cassandra"
```