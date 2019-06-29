#!/usr/bin/env python

from wield_services.deploy.slate.wield.slate_deploy import slate_wield
from wielder.wield.planner import WieldAction


if __name__ == "__main__":

    slate_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
