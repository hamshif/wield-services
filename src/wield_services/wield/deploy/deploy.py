#!/usr/bin/env python

from wielder.wield.modality import WieldServiceMode
from wielder.wield.planner import WieldAction
from wielder.wield.wield_project import WieldProject
from wield_services.wield.deploy.util import get_locale
from wield_services.deploy.slate.wield.slate_deploy import slate_wield
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield
from wield_services.wield.deploy.configurer import get_project_conf

import rx
import concurrent.futures


service_call_map = {
    'slate': slate_wield,
    'whisperer': whisperer_wield
}


def output(result):

    print(f"Type of result: {type(result)}")
    # [print(f"result: {r}") for r in result]
    print(result)


def micros_wield(parallel=True, action=None, delete_project_res=False):

    wield_mode, conf, action = get_project_conf(action)

    locale = get_locale(__file__)

    print('\nAttempting to create project level kubernetes resources e.g. namespaces\n')

    project = WieldProject(
        name='project',
        locale=locale,
        conf=conf,
        mode=wield_mode
    )

    if action == WieldAction.DELETE and not delete_project_res:
        print('skipping deletion of project level cluster resources such as namespaces')
    else:
        project.plan.wield(
            action=action,
            auto_approve=True
        )

    deployments = conf.deployments

    init_tuples = []

    for deploy in deployments:

        conf_service_mode = conf[deploy].WieldServiceMode

        service_mode = WieldServiceMode(
            observe=conf_service_mode.observe,
            service_only=conf_service_mode.service_only,
            debug_mode=conf_service_mode.debug_mode,
            local_mount=conf_service_mode.local_mount
        )

        init_tuples.append((service_call_map[deploy], service_mode))

    if parallel:

        with concurrent.futures.ProcessPoolExecutor(len(init_tuples)) as executor:
            rx.Observable.from_(init_tuples).flat_map(
                lambda s: executor.submit(
                    s[0],
                    mode=wield_mode,
                    service_mode=s[1],
                    project_override=True,
                    action=action,
                    auto_approve=True
                )
            ).subscribe(output)

    else:

        for t in init_tuples:

            t[0](
                mode=wield_mode,
                service_mode=t[1],
                project_override=True,
                action=action,
                auto_approve=True
            )


if __name__ == "__main__":

    micros_wield(parallel=True)

