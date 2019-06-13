#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_conf
from wield_services.deploy.slate.wield.slate_deploy import slate_wield
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield


def destroy():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env
    deploy_env = kube_args.deploy_env

    conf = get_conf(
        runtime_env=runtime_env,
        deploy_env=deploy_env
    )

    print(conf)

    slate_wield(
        conf=conf,
        action=WieldAction.DELETE,
        auto_approve=True
    )

    whisperer_wield(
        conf=conf,
        action=WieldAction.DELETE,
        auto_approve=True
    )


def test():

    destroy()


if __name__ == "__main__":

    test()

