#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.wield_service import WieldService

from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_module_root


# TODO code use of service only
def slate_wield(mode=None, project_override=False, action=WieldAction.PLAN, auto_approve=False, service_only=False, observe_deploy=True):

    module_root = get_module_root(__file__)
    print(f"Module root: {module_root}")

    service = WieldService(
        name='slate',
        module_root=module_root,
        mode=mode,
        project_override=project_override
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test():

    slate_wield(action=WieldAction.PLAN)

    slate_wield(action=WieldAction.APPLY)

    slate_wield(
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()
    test()
