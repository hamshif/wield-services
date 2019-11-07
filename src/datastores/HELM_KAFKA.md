
Helm 

```
brew install kubernetes-helm
```

Chart for Kafka

https://github.com/helm/charts/tree/master/incubator/kafka

```
helm init --history-max 200
helm repo add incubator http://storage.googleapis.com/kubernetes-charts-incubator
kubectl create ns kafka
helm install --name wielder-kafka --namespace kafka incubator/kafka 
helm install --name wielder-kafka --namespace kafka incubator/kafka --set replicas=1

helm install --name wielder-kafka --namespace kafka incubator/kafka --set replicas=1 --set envOverrides={zookeeper.replicaCount:1}
```

```
helm delete --purge wielder-kafka
```