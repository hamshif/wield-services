#!/usr/bin/env python
import logging
import os

from wield_services.wield.deploy.util import get_locale
from wield_services.wield.log_util import setup_logging
from wielder.wield.deployer import apply_multiple
from wielder.wield.enumerator import KubeResType


def get_ordered_cluster_res():

    res = [
        '00-namespace.yml',
        'variants/docker-desktop/docker-storage.yaml',
        'rbac-namespace-default/node-reader.yml',
        'rbac-namespace-default/pod-labler.yml',
        'variants/docker-desktop/default-privilege-add.yaml',
    ]

    return res


def get_ordered_zoo_res():

    namespace = 'kafka'
    zoo_res = [
        ('', namespace, 'zookeeper/10zookeeper-config.yml', KubeResType.GENERAL),
        ('pzoo', namespace, 'zookeeper/20pzoo-service.yml', KubeResType.SERVICE),
        ('zoo', namespace, 'zookeeper/21zoo-service.yml', KubeResType.SERVICE),
        ('zookeeper', namespace, 'zookeeper/30service.yml', KubeResType.SERVICE),
        ('pzoo', namespace, 'zookeeper/50pzoo.yml', KubeResType.STATEFUL_SET),
        ('zoo', namespace, 'zookeeper/51zoo.yml', KubeResType.STATEFUL_SET),
    ]

    return zoo_res


def get_ordered_kafka_res():

    namespace = 'kafka'
    kafka_res = [
        ('', namespace, 'kafka/10broker-config.yml', KubeResType.GENERAL),
        ('', namespace, 'kafka/20dns.yml', KubeResType.GENERAL),
        ('bootstrap', namespace, 'kafka/30bootstrap-service.yml', KubeResType.SERVICE),
        # ('kafka', namespace, 'kafka/50kafka.yml', KubeResType.DEPLOY),
        ('kafka', namespace, 'kafka/kafka-deploy.yaml', KubeResType.DEPLOY),
    ]

    return kafka_res


def kafka_wield():

    locale = get_locale(__file__)

    logging.debug('break')

    module_root = f'{locale.datastores_root}kubernetes-kafka'

    res = get_ordered_cluster_res()

    for r in res:
        os.system(f'kubectl apply -f {module_root}/{r}')

    zoo_res = get_ordered_zoo_res()

    apply_multiple(res_tuples=zoo_res, module_root=module_root)

    kafka_res = get_ordered_kafka_res()

    apply_multiple(res_tuples=kafka_res, module_root=module_root)


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    kafka_wield()



