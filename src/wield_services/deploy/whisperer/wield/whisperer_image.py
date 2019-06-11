#!/usr/bin/env python

from wield_services.wield.deploy.util import pack_image, get_conf


def whisperer_image():
    _conf = get_conf()
    # TODO add tag
    pack_image(_conf, base_name='py37', name='flask', push=False, force_base=False)

    # push_image(conf)


if __name__ == "__main__":

    whisperer_image()
