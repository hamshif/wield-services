#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.wield_service import WieldService
from wielder.wield.modality import WieldMode, WieldServiceMode
from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_locale


def slate_wield(mode=None, service_mode=None, project_override=False,
                action=WieldAction.PLAN, auto_approve=False, local_mount=False):

    locale = get_locale(__file__)

    if not mode:

        kube_parser = get_kube_parser()
        kube_args = kube_parser.parse_args()

        mode = WieldMode(
            runtime_env=kube_args.runtime_env,
            deploy_env=kube_args.deploy_env
        )

    if not service_mode:

        service_mode = WieldServiceMode(
            observe=True,
            service_only=True,
            debug_mode=True,
            local_mount=local_mount,
        )

    service = WieldService(
        name='slate',
        locale=locale,
        mode=mode,
        service_mode=service_mode,
        project_override=project_override
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test(local_mount=False):

    slate_wield(
        action=WieldAction.PLAN,
        local_mount=local_mount
    )

    slate_wield(
        action=WieldAction.APPLY,
        local_mount=local_mount
    )

    slate_wield(
        action=WieldAction.DELETE,
        auto_approve=False
    )


if __name__ == "__main__":

    test(
        local_mount=True
    )
