#!/usr/bin/env python
import logging

from wield_services.wield.log_util import setup_logging
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

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    test(
        local_mount=False
    )
