#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.wield_service import WieldService
from wielder.wield.modality import WieldMode, WieldServiceMode
from wielder.wield.planner import WieldAction
from wielder.wield.wield_service import get_module_root
from wield_services.wield.deploy.util import get_project_root, get_super_project_root


def slate_wield(mode=None, service_mode=None, project_override=False, action=WieldAction.PLAN, auto_approve=False):

    module_root = get_module_root(__file__)
    print(f"Module root: {module_root}")

    project_root = get_project_root()
    super_project_root = get_super_project_root()

    service = WieldService(
        name='slate',
        module_root=module_root,
        project_root=project_root,
        super_project_root=super_project_root,
        mode=mode,
        service_mode=service_mode,
        project_override=project_override
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test(runtime_env='docker', local_mount=False):

    mode = WieldMode(
        runtime_env=runtime_env,
        deploy_env='dev'
    )

    service_mode = WieldServiceMode(
        observe=True,
        service_only=True,
        debug_mode=True,
        local_mount=local_mount,
    )

    slate_wield(
        mode=mode,
        service_mode=service_mode,
        action=WieldAction.PLAN
    )

    slate_wield(
        mode=mode,
        service_mode=service_mode,
        action=WieldAction.APPLY
    )

    slate_wield(
        mode=mode,
        service_mode=service_mode,
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    test(
        runtime_env=kube_args.runtime_env,
        local_mount=False
    )
