#!/usr/bin/env python

from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield
from wielder.wield.planner import WieldAction

if __name__ == "__main__":

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
