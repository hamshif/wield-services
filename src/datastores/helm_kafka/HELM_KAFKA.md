
Helm 

```
brew install kubernetes-helm
```

Chart for Kafka

https://github.com/helm/charts/tree/master/incubator/kafka

Helm older version needed for this installation !!!
===========
https://medium.com/@schmijos/installing-old-homebrew-formulas-dc91de0c329c

```
helm init
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
kubectl create ns kafka
helm install --name wielder-kafka --namespace kafka incubator/kafka 

helm install --name wielder-kafka --namespace kafka incubator/kafka --set replicas=1

helm install --name wielder-kafka --namespace kafka incubator/kafka --set replicas=1 --set envOverrides={zookeeper.replicaCount:1}


helm install --name wielder-kafka --namespace kafka incubator/kafka --set configurationOverride="{"replica.fetch.max.bytes":15048576,"message.max.bytes":15048576}"
```

```
helm delete --purge wielder-kafka
```