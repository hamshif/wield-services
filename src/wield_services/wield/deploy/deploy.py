#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wield_services.wield.deploy.util import get_conf


def wield():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env
    deploy_env = kube_args.deploy_env

    conf = get_conf(
        runtime_env=runtime_env,
        deploy_env=deploy_env
    )

    print(conf)


def test():

    wield()


if __name__ == "__main__":

    test()

