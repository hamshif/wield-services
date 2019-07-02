#!/usr/bin/env python

from wielder.wield.wield_project import get_conf_context_project
from wield_services.wield.deploy.util import get_project_root


# TODO add framework tests to project

def t_runtime_env():

    project_root = get_project_root()
    env_gcp = get_conf_context_project(
        project_root=project_root,
        runtime_env='gcp'
    )
    env_docker = get_conf_context_project(
        project_root=project_root,
        runtime_env='docker'
    )

    if env_gcp.food == 'falafel' and env_docker.food == 'schnitzel':
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


if __name__ == "__main__":

    t_override()
    t_runtime_env()
    t_deploy_env()

