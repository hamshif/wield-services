#!/usr/bin/env python
import logging

from wield_services.deploy.boot.wield.boot_deploy import boot_wield
from wield_services.wield.log_util import setup_logging
from wielder.wield.planner import WieldAction


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    boot_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
