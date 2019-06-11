#!/usr/bin/env python

from wield_services.wield.deploy.util import pack_image, get_conf, get_module_root


def slate_image():

    conf = get_conf()

    pack_image(
        conf,
        name='py37',
        push=False,
        force=False
    )

    module_root = get_module_root(__file__)

    image_root = f'{module_root}image'

    pack_image(
        conf,
        name='slate',
        push=False,
        force=True,
        image_root=image_root
    )

    # push_image(conf)


if __name__ == "__main__":

    slate_image()
