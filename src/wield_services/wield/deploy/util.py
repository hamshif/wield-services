#!/usr/bin/env python
import os
from wielder.util.arguer import get_kube_parser
from wielder.util.commander import async_cmd
from wielder.wield.wield_project import get_module_root, get_conf_context_project
from wielder.wield.locale import Locale


RUNTIME_ENV = 'RUNTIME_ENV'


def get_super_project_root():

    super_project_root = get_project_root()

    for i in range(5):
        super_project_root = super_project_root[:super_project_root.rfind('/')]

    return super_project_root


def get_project_root():

    return get_module_root(__file__)


def get_project_image_root():

    module_root = get_module_root(__file__)[:-1]

    image_root = module_root[:module_root.rfind('/') + 1] + 'image'

    return image_root


def get_locale(__file__1):

    module_root = get_module_root(__file__1)
    print(f"Module root: {module_root}")

    project_root = get_project_root()
    super_project_root = get_super_project_root()

    locale = Locale(
        project_root=project_root,
        super_project_root=super_project_root,
        module_root=module_root,
        code_path=None
    )

    return locale


# TODO add framework tests to project
def t_runtime_env():

    project_root = get_project_root()
    env_gke = get_conf_context_project(
        project_root=project_root,
        runtime_env='gke'
    )
    env_docker = get_conf_context_project(
        project_root=project_root,
        runtime_env='docker'
    )

    if env_gke.food == 'falafel' and env_docker.food == 'schnitzel':
        print('cool')
    else:
        print('aww')


def t_deploy_env():

    project_root = get_project_root()
    env_dev = get_conf_context_project(
        project_root=project_root,
        deploy_env='dev'
    )

    env_int = get_conf_context_project(
        project_root=project_root,
        deploy_env='int'
    )

    if env_dev.kube_context == 'docker-for-desktop' and env_int.kube_context == 'int-gke':
        print('\ndeploy_env cool')
    else:
        print('\ndeploy_env aww')


def t_override():

    project_root = get_project_root()
    env_dev = get_conf_context_project(
        project_root=project_root,
        deploy_env='dev'
    )

    account = env_dev.providers.gcp.service_account

    if 'dev' in account:
        print('\noverride cool')
    else:
        print('\noverride aww')


def test():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env

    project_root = get_project_root()
    get_conf_context_project(
        project_root=project_root,
        runtime_env=runtime_env
    )


if __name__ == "__main__":

    get_super_project_root()

    test()
    # t_override()
    # t_runtime_env()
    # t_deploy_env()

