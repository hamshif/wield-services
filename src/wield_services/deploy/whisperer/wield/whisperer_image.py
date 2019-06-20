#!/usr/bin/env python

from wield_services.wield.deploy.util import pack_image, get_conf_context_project, get_module_root


def whisperer_image():

    conf = get_conf_context_project()

    pack_image(
        conf,
        name='py37',
        push=False,
        force=False
    )

    pack_image(
        conf,
        name='flask',
        push=False,
        force=True
    )

    # push_image(conf)


if __name__ == "__main__":

    whisperer_image()
