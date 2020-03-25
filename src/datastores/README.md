This module wraps third party software e.g. Kafka, datastores etc...
=


Cassandra
-

https://github.com/helm/charts/tree/master/incubator/cassandra


```
helm install --namespace "cassandra" -n "cassandra" incubator/cassandra
helm status "cassandra"
helm delete  --purge "cassandra"
```