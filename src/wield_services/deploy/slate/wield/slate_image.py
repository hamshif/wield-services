#!/usr/bin/env python

from wielder.util.imager import pack_image
from wield_services.wield.deploy.util import get_conf_context_project, \
    get_module_root, get_project_image_root, get_project_root


def slate_image():

    project_root = get_project_root()
    conf = get_conf_context_project(project_root=project_root)

    pack_image(
        conf=conf,
        name='py37',
        image_root=get_project_image_root(),
        push=False,
        force=False,
        tag='dev'
    )

    module_root = get_module_root(__file__)

    image_root = f'{module_root}image'

    code_path = f'{image_root}/code_path'

    pack_image(
        conf,
        name='slate',
        image_root=image_root,
        push=False,
        force=True,
        tag='dev',
        mount=True
    )

    # push_image(conf)


if __name__ == "__main__":

    slate_image()
