#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser

from wielder.wield.planner import WieldPlan, WieldAction
from wield_services.wield.deploy.util import get_module_root


# TODO code use of service only
def slate_wield(conf, action=WieldAction.PLAN, auto_approve=False, service_only=False, observe_deploy=True):

    if conf:
        runtime_env = conf.runtime_env
    else:
        # TODO get conf myself
        runtime_env = 'docker'

    module_root = get_module_root(__file__)
    print(f"Module root: {module_root}")

    conf_dir = f'{module_root}conf'
    print(f"conf_path: {conf_dir}")

    plan_dir = f'{module_root}plan'
    print(f"plan_path: {plan_dir}")

    plan = WieldPlan(
        name='slate',
        conf_dir=conf_dir,
        plan_dir=plan_dir,
        runtime_env=runtime_env
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

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()
    test()
