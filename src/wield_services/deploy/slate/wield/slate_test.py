#!/usr/bin/env python

from wielder.wield.planner import WieldAction
from wield_services.deploy.slate.wield.slate_deploy import slate_wield


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
        local_mount=False
    )
