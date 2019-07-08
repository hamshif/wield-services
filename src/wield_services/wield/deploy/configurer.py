#!/usr/bin/env python
from wielder.util.arguer import get_kube_parser
from wielder.wield.wield_project import get_wield_mode

from wield_services.wield.deploy.util import get_project_root
from wield_services.wield.deploy.util import get_conf_context_project


def get_project_conf(action=None):

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    print(kube_args)

    runtime_env = kube_args.runtime_env
    deploy_env = kube_args.deploy_env

    project_root = get_project_root()

    wield_mode = get_wield_mode(
        project_root=project_root,
        runtime_env=runtime_env,
        deploy_env=deploy_env
    )

    conf = get_conf_context_project(
        project_root=project_root,
        runtime_env=wield_mode.runtime_env,
        deploy_env=wield_mode.deploy_env
    )

    print(conf)

    if not action:
        action = kube_args.wield

    return wield_mode, conf, action
