#!/usr/bin/env python
import os

from wielder.util.arguer import get_kube_parser
from wielder.wield.deployer import init_observe_pods

from pyhocon import ConfigFactory as Cf
from pyhocon.tool import HOCONConverter


def slate_deploy_init_callback(result):

    for i in range(len(result)):

        print(f"{i}: slate deploy result returned: {result[i]}")


def get_module_root():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    module_root = dir_path[:dir_path.rfind('/') + 1]
    print(f"Module root: {module_root}")

    return module_root


def wrap_included(paths):

    includes = ''
    for path in paths:
        includes += wrap_include(path)

    return includes


def wrap_include(path):

    wrapped = f'include file("{path}")\n'

    return wrapped


def plan(plans):

    for pl in plans:

        with open(pl[0], "wt") as file_out:
            file_out.write(pl[1])


def slate_deploy():

    module_root = get_module_root()
    print(f"Module root: {module_root}")

    conf_path = f'{module_root}conf'
    print(f"conf_path: {conf_path}")

    plan_path = f'{module_root}plan'
    print(f"plan_path: {plan_path}")

    env = 'docker'
    apply_kube = True
    plan_format = 'yaml'

    vars_conf_path = f'{conf_path}/{env}/slate-vars.conf'
    storage_conf_path = f'{conf_path}/{env}/slate-storage.conf'
    pv_conf_path = f'{conf_path}/slate-pv.conf'
    pvc_conf_path = f'{conf_path}/slate-pvc.conf'
    deploy_file_path = f'{conf_path}/slate-deploy.conf'

    confs = [vars_conf_path, storage_conf_path, pv_conf_path, pvc_conf_path, deploy_file_path]

    included = wrap_included(confs)

    print(f'\nincluded: {included}')

    conf = Cf.parse_string(included)

    storage_plan = HOCONConverter.convert(conf.storage, plan_format, 2)
    pv_plan = HOCONConverter.convert(conf.pv, plan_format, 2)
    pvc_plan = HOCONConverter.convert(conf.pvc, plan_format, 2)
    deploy_plan = HOCONConverter.convert(conf.deploy, plan_format, 2)

    print(f'\n{storage_plan}')
    print(f'\n{pv_plan}')
    print(f'\n{pvc_plan}')
    print(f'\n{deploy_plan}')

    plans1 = [
        (f'{plan_path}/slate-storage.{plan_format}', storage_plan),
        (f'{plan_path}/slate-pv.{plan_format}', pv_plan),
        (f'{plan_path}/slate-pvc.{plan_format}', pvc_plan),
        (f'{plan_path}/slate-deploy.{plan_format}', deploy_plan)
    ]

    plan(plans1)

    for pl in plans1:

        os.system(f"kubectl apply -f {pl[0]};")

    # Observe the pods created
    init_observe_pods(
        deploy_tuple=('slate', f'{plan_path}/slate-deploy.{plan_format}'),
        use_minikube_repo=False,
        callback=slate_deploy_init_callback,
        init=False
    )


if __name__ == "__main__":

    slate_deploy()

