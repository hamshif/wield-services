#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.planner import WieldAction
from wielder.wield.modality import WieldMode
from wield_services.wield.deploy.util import get_conf_context_project
from wield_services.deploy.slate.wield.slate_deploy import slate_wield
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield
from wield_services.wield.deploy.util import get_project_root

import rx
import concurrent.futures


def output(result):

    print(f"Type of result: {type(result)}")
    # [print(f"result: {r}") for r in result]
    print(result)


def micros_deploy(local_mount=False):

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env if kube_args.runtime_env else 'docker'
    deploy_env = kube_args.deploy_env if kube_args.deploy_env else 'dev'

    project_root = get_project_root()

    conf = get_conf_context_project(
        project_root=project_root,
        runtime_env=runtime_env,
        deploy_env=deploy_env
    )

    mode = WieldMode(
        runtime_env=runtime_env,
        deploy_env=deploy_env,
        debug_mode=True,
        local_mount=local_mount
    )

    print(conf)

    init_functions = [slate_wield, whisperer_wield]

    with concurrent.futures.ProcessPoolExecutor(len(init_functions)) as executor:
        rx.Observable.from_(init_functions).flat_map(
            lambda s: executor.submit(
                s,
                mode=mode,
                project_override=True,
                action=WieldAction.APPLY,
                auto_approve=True,
                service_only=False,
                observe_deploy=True
            )
        ).subscribe(output)

    # slate_wield(
    #     mode=mode,
    #     project_override=True,
    #     action=WieldAction.APPLY,
    #     auto_approve=True,
    #     service_only=False,
    #     observe_deploy=True
    # )

    # whisperer_wield(
    #     mode=mode,
    #     project_override=True,
    #     action=WieldAction.APPLY,
    #     auto_approve=True,
    #     service_only=False,
    #     observe_deploy=True
    # )


def test():

    micros_deploy(local_mount=False)


if __name__ == "__main__":

    test()

