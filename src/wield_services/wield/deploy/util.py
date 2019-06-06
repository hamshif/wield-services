#!/usr/bin/env python
import os
from wielder.util.arguer import get_kube_parser
from pyhocon import ConfigFactory as Cf
from wielder.wield.planner import wrap_included

RUNTIME_ENV = 'RUNTIME_ENV'


def get_conf(runtime_env='docker', deploy_env='dev'):
    """
    Gets the configuration from environment specific config.
    Config files gateways [specific include statements] have to be placed and named according to convention.
    :param deploy_env: Development stage [dev, int, qa, stage, prod]
    :param runtime_env: Where the kubernetes cluster is running
    :return: pyhocon configuration tree object
    :except: If both data_conf_env are not None
    """

    module_root = get_module_root(__file__)

    project_conf_path = f'{module_root}conf/project.conf'
    runtime_conf_path = f'{module_root}conf/runtime_env/{runtime_env}/wield.conf'
    deploy_env_conf_path = f'{module_root}conf/deploy_env/{deploy_env}/wield.conf'
    developer_conf_path = f'{module_root}conf/personal/developer.conf'

    conf_include_string = wrap_included([
        project_conf_path,
        runtime_conf_path,
        deploy_env_conf_path,
        developer_conf_path
    ])

    print(f"\nconf_include_string:  {conf_include_string}\n")

    conf = Cf.parse_string(conf_include_string)

    print(conf)

    return conf


def get_module_root(file_context=__file__):

    dir_path = os.path.dirname(os.path.realpath(file_context))
    print(f"\ncurrent working dir: {dir_path}\n")

    module_root = dir_path[:dir_path.rfind('/') + 1]
    print(f"Module root: {module_root}")

    return module_root


# TODO add framework tests to project
def t_runtime_env():

    env_gke = get_conf(runtime_env='gke')
    env_docker = get_conf(runtime_env='docker')

    if env_gke.food == 'falafel' and env_docker.food == 'schnitzel':
        print('cool')
    else:
        print('aww')


def t_deploy_env():

    env_dev = get_conf(deploy_env='dev')
    env_int = get_conf(deploy_env='int')

    if env_dev.kube_context == 'docker-for-desktop' and env_int.kube_context == 'int-gke':
        print('\ndeploy_env cool')
    else:
        print('\ndeploy_env aww')


def t_override():

    env_dev = get_conf(deploy_env='dev')

    account = env_dev.providers.gcp.service_account

    if 'dev' in account:
        print('\noverride cool')
    else:
        print('\noverride aww')


def test():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env

    get_conf(runtime_env=runtime_env)


if __name__ == "__main__":

    test()
    # t_override()
    # t_runtime_env()
    # t_deploy_env()
