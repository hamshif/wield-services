#!/usr/bin/env python
import os
from enum import Enum

from wield_services.wield.deploy.util import get_locale
from wielder.wrx.deployer import get_pods, observe_pod, delete_pv
from wielder.wrx.servicer import observe_service


class ResType(Enum):

    GENERAL = 'general'
    STORAGE = 'storageclasses'
    DEPLOY = 'deploy'
    SERVICE = 'svc'
    STATEFUL_SET = 'statefulsets'
    PV = 'pv'


def delete(res_tuples, module_root):

    for res_tup in res_tuples:
        name, namespace, res_path, _type = res_tup

        if _type == ResType.PV:

            delete_pv(namespace=namespace, pv_type=name)
        else:
            os.system(f'kubectl delete -f {module_root}/{res_path} --wait=false;')

            if _type == ResType.DEPLOY or _type == ResType.STATEFUL_SET:

                pods = get_pods(
                    name,
                    namespace=namespace
                )

                for pod in pods:
                    os.system(f"kubectl delete -n {namespace} {pod} --force --grace-period=0;")


def apply(res_tuples, module_root, observe_svc=False):

    for res_tup in res_tuples:
        name, namespace, res_path, _type = res_tup

        os.system(f'kubectl apply -f {module_root}/{res_path}')

        if _type == ResType.SERVICE and observe_svc:

            observe_service(
                svc_name=name,
                svc_namespace=namespace
            )

        elif _type == ResType.DEPLOY or _type == ResType.STATEFUL_SET:

            pods = get_pods(
                name,
                namespace=namespace
            )

            for pod in pods:
                observe_pod(pod)


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
        ('', namespace, 'zookeeper/10zookeeper-config.yml', ResType.GENERAL),
        ('pzoo', namespace, 'zookeeper/20pzoo-service.yml', ResType.SERVICE),
        ('zoo', namespace, 'zookeeper/21zoo-service.yml', ResType.SERVICE),
        ('zookeeper', namespace, 'zookeeper/30service.yml', ResType.SERVICE),
        ('pzoo', namespace, 'zookeeper/50pzoo.yml', ResType.STATEFUL_SET),
        ('zoo', namespace, 'zookeeper/51zoo.yml', ResType.STATEFUL_SET),
    ]

    return zoo_res


def get_ordered_kafka_res():

    namespace = 'kafka'
    kafka_res = [
        ('', namespace, 'kafka/10broker-config.yml', ResType.GENERAL),
        ('', namespace, 'kafka/20dns.yml', ResType.GENERAL),
        ('bootstrap', namespace, 'kafka/30bootstrap-service.yml', ResType.SERVICE),
        ('kafka', namespace, 'kafka/50kafka.yml', ResType.DEPLOY),
    ]

    return kafka_res


def kafka_wield():

    locale = get_locale(__file__)

    print('break')

    module_root = f'{locale.datastores_root}kubernetes-kafka'

    res = get_ordered_cluster_res()

    for r in res:
        os.system(f'kubectl apply -f {module_root}/{r}')

    zoo_res = get_ordered_zoo_res()

    apply(res_tuples=zoo_res, module_root=module_root)

    kafka_res = get_ordered_kafka_res()

    apply(res_tuples=kafka_res, module_root=module_root)


if __name__ == "__main__":

    kafka_wield()



