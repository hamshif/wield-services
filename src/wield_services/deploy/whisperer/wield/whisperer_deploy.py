#!/usr/bin/env python

from wielder.wield.wield_service import WieldService
from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_module_root


# TODO code or configure to use of service only
def whisperer_wield(mode=None, project_override=False, action=WieldAction.PLAN, auto_approve=False, service_only=False, observe_deploy=True):

    module_root = get_module_root(__file__)
    print(f"Module root: {module_root}")

    service = WieldService(
        name='whisperer',
        module_root=module_root,
        mode=mode,
        project_override=project_override
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test():

    whisperer_wield(action=WieldAction.PLAN)

    whisperer_wield(action=WieldAction.APPLY)

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    test()
