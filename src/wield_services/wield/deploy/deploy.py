#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_conf
from wield_services.deploy.slate.wield.slate_deploy import slate_wield
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield

import rx
import concurrent.futures


def output(result):

    print(f"Type of result: {type(result)}")
    # [print(f"result: {r}") for r in result]
    print(result)


def micros_deploy():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env
    deploy_env = kube_args.deploy_env

    conf = get_conf(
        runtime_env=runtime_env,
        deploy_env=deploy_env
    )

    print(conf)

    init_functions = [slate_wield, whisperer_wield]

    with concurrent.futures.ProcessPoolExecutor(len(init_functions)) as executor:
        rx.Observable.from_(init_functions).flat_map(
            lambda s: executor.submit(
                s, conf, WieldAction.APPLY, auto_approve=True, service_only=False, observe_deploy=True
            )
        ).subscribe(output)

    # slate_wield(
    #     action=WieldAction.APPLY,
    #     auto_approve=True
    # )
    #
    # whisperer_wield(
    #     action=WieldAction.APPLY,
    #     auto_approve=True
    # )


def test():

    micros_deploy()


if __name__ == "__main__":

    test()

