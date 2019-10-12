#!/usr/bin/env python

from wield_services.wield.deploy.util import get_locale, get_module_locale
from wield_services.wield.deploy.configurer import get_project_deploy_mode
from wielder.util.commander import async_cmd

#  TODO find a way to abstract this it's ugly
from wield_services.deploy.boot.wield.boot_image import boot_image
from wield_services.deploy.pep.wield.pep_image import pep_image
from wield_services.deploy.whisperer.wield.whisperer_image import whisperer_image
from wield_services.deploy.slate.wield.slate_image import slate_image


def output(result):

    print(f"Type of result: {type(result)}")
    # [print(f"result: {r}") for r in result]
    print(result)


def micros_image(parallel=True, action=None, delete_project_res=False):

    wield_mode, conf, action = get_project_deploy_mode(action)

    locale = get_locale(__file__)

    deployments = conf.deployments

    for deploy in deployments:

        print(f'{deploy}')

        module_root = get_module_locale(deploy).module_root

        image_script = f'{module_root}wield/{deploy}_image.py'

        print(f'{image_script}')


if __name__ == "__main__":

    # micros_image(parallel=True)
    boot_image()
    whisperer_image()
    slate_image()
    pep_image()




