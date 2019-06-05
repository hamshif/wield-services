#!/usr/bin/env python
import os
from wielder.util.arguer import get_kube_parser

from wielder.wield.planner import WieldPlan, WieldAction


def get_module_root():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")

    module_root = dir_path[:dir_path.rfind('/') + 1]
    print(f"Module root: {module_root}")

    return module_root


# TODO code use of service only and observe
def slate_wield(action=WieldAction.PLAN, auto_approve=False, service_only=False, observe=True):

    module_root = get_module_root()
    print(f"Module root: {module_root}")

    conf_dir = f'{module_root}conf'
    print(f"conf_path: {conf_dir}")

    plan_dir = f'{module_root}plan'
    print(f"plan_path: {plan_dir}")

    plan = WieldPlan(
        name='slate',
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

    slate_wield(WieldAction.PLAN)

    slate_wield(WieldAction.APPLY)

    slate_wield(
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    test()
