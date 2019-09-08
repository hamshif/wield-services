#!/usr/bin/env python

from wield_services.deploy.pep.wield.pep_deploy import pep_wield
from wielder.wield.planner import WieldAction


if __name__ == "__main__":

    pep_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
