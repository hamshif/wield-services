#!/usr/bin/env python

from wielder.util.arguer import ensure_action_and_mode_from_args
from wielder.wield.wield_project import WieldService
from wielder.wield.modality import WieldServiceMode
from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.util import get_locale


def whisperer_wield(mode=None, service_mode=None, project_override=False,
                    action=None, auto_approve=False, local_mount=False):

    locale = get_locale(__file__)

    action, mode = ensure_action_and_mode_from_args(action, mode)

    if not service_mode:

        service_mode = WieldServiceMode(
            observe=True,
            service_only=True,
            debug_mode=True,
            local_mount=local_mount,
            project_override=project_override
        )

    service = WieldService(
        name='whisperer',
        locale=locale,
        mode=mode,
        service_mode=service_mode
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve
    )


def test(local_mount=False):

    whisperer_wield(
        action=WieldAction.PLAN,
        local_mount=local_mount
    )

    whisperer_wield(
        action=WieldAction.APPLY,
        local_mount=local_mount
    )

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=False,
        local_mount=local_mount
    )


if __name__ == "__main__":

    whisperer_wield(
        local_mount=True
    )

    # test(
    #     local_mount=True
    # )
