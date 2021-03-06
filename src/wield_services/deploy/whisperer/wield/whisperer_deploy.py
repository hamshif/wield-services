#!/usr/bin/env python
import logging

from wield_services.wield.log_util import setup_logging
from wielder.util.arguer import replace_none_vars_from_args
from wielder.wield.wield_service import WieldService
from wield_services.wield.deploy.util import get_locale


def whisperer_wield(action=None, auto_approve=False, service_only=False):

    locale = get_locale(__file__)

    action, mode, enable_debug, local_mount, service_mode = replace_none_vars_from_args(
        action=action,
        mode=None,
        enable_debug=None,
        local_mount=None,
        service_mode=None,
        project_override=None
    )

    service = WieldService(
        name='whisperer',
        locale=locale,
        mode=mode,
        service_mode=service_mode,
    )

    service.plan.wield(
        action=action,
        auto_approve=auto_approve,
        service_only=service_only
    )


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    whisperer_wield()
