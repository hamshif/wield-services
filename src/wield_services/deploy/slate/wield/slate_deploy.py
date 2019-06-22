#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.wield_service import WieldService
from wielder.wield.modality import WieldMode
from wielder.wield.planner import WieldAction
from wielder.wield.wield_service import get_module_root
from wield_services.wield.deploy.util import get_project_root


# TODO code use of service only
def slate_wield(
        mode=None, project_override=False, action=WieldAction.PLAN,
        auto_approve=False, service_only=False, observe_deploy=True):

    module_root = get_module_root(__file__)
    print(f"Module root: {module_root}")

    project_root = get_project_root()

    service = WieldService(
        name='slate',
        module_root=module_root,
        project_root=project_root,
        mode=mode,
        project_override=project_override
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test():

    mode = WieldMode(
        runtime_env='docker',
        deploy_env='dev',
        debug_mode=True,
        local_mount=True
    )

    slate_wield(
        mode=mode,
        action=WieldAction.PLAN
    )

    slate_wield(
        mode=mode,
        action=WieldAction.APPLY
    )

    slate_wield(
        mode=mode,
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()
    test()
