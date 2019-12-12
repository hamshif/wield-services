#!/usr/bin/env python
import os

from wield_services.wield.deploy.util import get_locale
from wielder.wield.deployer import delete_pvc_pv, delete_multiple
from wield_services.third_party.kafka.wield.kafka_deploy import get_ordered_cluster_res, get_ordered_zoo_res, get_ordered_kafka_res


def kafka_delete(del_cluster_assets=False, del_pv=True):

    namespace = 'kafka'
    locale = get_locale(__file__)

    print('point')

    module_root = f'{locale.datastores_root}kubernetes-kafka'

    kafka_res = get_ordered_kafka_res()
    delete_multiple(res_tuples=kafka_res, module_root=module_root)

    zoo_res = get_ordered_zoo_res()
    delete_multiple(res_tuples=zoo_res, module_root=module_root)

    if del_pv:
        os.system(f'kubectl delete -f {module_root}/variants/docker-desktop/docker-storage.yaml --wait=false')
        print('tsav')
        delete_pvc_pv('data-kafka', namespace=namespace)
        print('mamoota')
        delete_pvc_pv('data-zoo', namespace=namespace)
        print('arnav')
        delete_pvc_pv('data-pzoo', namespace=namespace)

    if del_cluster_assets:

        res = get_ordered_cluster_res()

        for r in reversed(res):
            os.system(f'kubectl delete -f {module_root}/{r} --wait=false')


if __name__ == "__main__":

    print()
    kafka_delete()



