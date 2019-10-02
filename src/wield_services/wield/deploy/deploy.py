#!/usr/bin/env python

from wielder.util.arguer import replace_none_vars_from_args
from wielder.util.commander import async_cmd
from wielder.wield.wield_service import WieldService
from wielder.wield.modality import WieldServiceMode
from wielder.wield.planner import WieldAction
from wielder.wield.wield_project import WieldProject
from wield_services.wield.deploy.util import get_locale, get_module_locale
from wield_services.wield.deploy.configurer import get_project_deploy_mode

import rx
import concurrent.futures


def launch_service(
        name, mode=None, service_mode=None, project_override=False,
        action=None, auto_approve=False, service_only=False,
        enable_debug=None, local_mount=None):

    svc_locale = get_module_locale(name)

    action, mode, enable_debug, local_mount, service_mode = replace_none_vars_from_args(
        action=action,
        mode=mode,
        enable_debug=enable_debug,
        local_mount=local_mount,
        service_mode=service_mode,
        project_override=project_override
    )

    service = WieldService(
        name=name,
        locale=svc_locale,
        mode=mode,
        service_mode=service_mode,
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve,
        service_only=service_only
    )


def output(result):

    print(f"Type of result: {type(result)}")
    # [print(f"result: {r}") for r in result]
    print(result)


# TODO expand this and make it generic for installation types
def installations(installations):

    installations.helm

    [print(installation) for installation in installations]

    if 'kafka' in installations.helm:

        async_cmd('kubectl create ns kafka')
        async_cmd('helm install --name wielder-kafka --namespace kafka incubator/kafka')

#         TODO wait and monitor helm installation completed using kubectl output



def micros_wield(parallel=True, action=None, delete_project_res=False):

    wield_mode, conf, action = get_project_deploy_mode(action)

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
        
        installations(project.conf.installations)
        
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

        init_tuples.append((launch_service, deploy, service_mode))

    if parallel:

        with concurrent.futures.ProcessPoolExecutor(len(init_tuples)) as executor:
            rx.Observable.from_(init_tuples).flat_map(
                lambda s: executor.submit(
                    s[0],
                    name=s[1],
                    mode=wield_mode,
                    service_mode=s[2],
                    project_override=True,
                    action=action,
                    auto_approve=True
                )
            ).subscribe(output)

    else:

        for t in init_tuples:

            t[0](
                name=t[1],
                mode=wield_mode,
                service_mode=t[2],
                project_override=True,
                action=action,
                auto_approve=True
            )


if __name__ == "__main__":

    micros_wield(parallel=True)

