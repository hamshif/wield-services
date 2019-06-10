#!/usr/bin/env python

from wielder.wield.planner import WieldAction
from wield_services.deploy.slate.wield.slate_deploy import slate_wield

if __name__ == "__main__":

    slate_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
