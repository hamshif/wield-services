#!/usr/bin/env python

from wielder.wield.planner import WieldAction
from wield_services.deploy.whisperer.wield.whisperer_deploy import whisperer_wield

if __name__ == "__main__":

    whisperer_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
