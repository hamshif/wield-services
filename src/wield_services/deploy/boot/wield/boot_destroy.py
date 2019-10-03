#!/usr/bin/env python

from wield_services.deploy.boot.wield.boot_deploy import boot_wield
from wielder.wield.planner import WieldAction


if __name__ == "__main__":

    boot_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
