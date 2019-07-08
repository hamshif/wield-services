#!/usr/bin/env python

from wielder.util.arguer import ensure_none_variables_from_args
from wielder.wield.wield_service import WieldService
from wield_services.wield.deploy.util import get_locale


#  TODO abstract this it is very repetitive
def whisperer_wield(
        mode=None, service_mode=None, project_override=False,
        action=None, auto_approve=False, service_only=False,
        enable_debug=None, local_mount=None):

    locale = get_locale(__file__)

    action, mode, enable_debug, local_mount, service_mode = ensure_none_variables_from_args(
        action=action,
        mode=mode,
        enable_debug=enable_debug,
        local_mount=local_mount,
        service_mode=service_mode,
        project_override=project_override
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

    whisperer_wield()
