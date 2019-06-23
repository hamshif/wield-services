#!/usr/bin/env python

from wielder.util.imager import pack_image
from wield_services.wield.deploy.util import get_conf_context_project, \
    get_module_root, get_project_image_root, get_project_root


def whisperer_image():

    project_root = get_project_root()
    conf = get_conf_context_project(project_root=project_root)
    image_root = get_project_image_root()

    pack_image(
        conf,
        name='py37',
        image_root=image_root,
        push=False,
        force=False,
        tag='dev'
    )

    pack_image(
        conf,
        name='flask',
        image_root=image_root,
        push=False,
        force=True,
        tag='dev'
    )

    # push_image(conf)


if __name__ == "__main__":

    whisperer_image()
