#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield
from wielder.wield.planner import WieldAction
from wielder.wield.modality import WieldMode


if __name__ == "__main__":

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env
    deploy_env = kube_args.deploy_env

    mode = WieldMode(
        runtime_env=runtime_env,
        deploy_env=deploy_env,
        debug_mode=True,
        local_mount=False
    )

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=True,
        mode=mode
    )
