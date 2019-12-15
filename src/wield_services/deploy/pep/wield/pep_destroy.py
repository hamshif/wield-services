#!/usr/bin/env python
import logging

from wield_services.deploy.pep.wield.pep_deploy import pep_wield
from wield_services.wield.log_util import setup_logging
from wielder.wield.planner import WieldAction


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    pep_wield(
        action=WieldAction.DELETE,
        auto_approve=True
    )
