#!/usr/bin/env python

from wielder.wield.planner import WieldAction
from wield_services.wield.deploy.deploy import micros_wield


def destroy():

    micros_wield(parallel=True, action=WieldAction.DELETE)
    # micros_wield(parallel=True, action=WieldAction.DELETE, delete_project_res=True)


if __name__ == "__main__":

    destroy()

