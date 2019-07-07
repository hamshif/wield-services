#!/usr/bin/env python

from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield
from wielder.wield.planner import WieldAction


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

    test(
        local_mount=False
    )
