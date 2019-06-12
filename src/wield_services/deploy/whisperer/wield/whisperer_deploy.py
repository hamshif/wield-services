#!/usr/bin/env python

from wielder.wield.planner import WieldPlan, WieldAction
from wield_services.wield.deploy.util import get_module_root


# TODO code use of service only
def whisperer_wield(action=WieldAction.PLAN, auto_approve=False, service_only=False, observe_deploy=True):

    module_root = get_module_root(__file__)
    print(f"Module root: {module_root}")

    conf_dir = f'{module_root}conf'
    print(f"conf_path: {conf_dir}")

    plan_dir = f'{module_root}plan'
    print(f"plan_path: {plan_dir}")

    plan = WieldPlan(
        name='whisperer',
        conf_dir=conf_dir,
        plan_dir=plan_dir,
        runtime_env='docker'
    )

    plan.pretty()

    plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test():

    whisperer_wield(WieldAction.PLAN)

    whisperer_wield(WieldAction.APPLY)

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    test()