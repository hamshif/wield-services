#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_conf_context_project
from wield_services.deploy.slate.wield.slate_deploy import slate_wield
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield
from wield_services.wield.deploy.util import get_project_root
from wielder.wield.modality import WieldMode


def destroy():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env
    deploy_env = kube_args.deploy_env

    project_root = get_project_root()

    conf = get_conf_context_project(
        project_root=project_root,
        runtime_env=runtime_env,
        deploy_env=deploy_env
    )

    print(conf)

    mode = WieldMode(
        runtime_env=runtime_env,
        deploy_env=deploy_env,
        debug_mode=True,
        local_mount=False
    )

    slate_wield(
        action=WieldAction.DELETE,
        auto_approve=True,
        mode=mode
    )

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=True,
        mode=mode
    )


if __name__ == "__main__":

    destroy()

