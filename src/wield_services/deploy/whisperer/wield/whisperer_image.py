#!/usr/bin/env python

from wielder.util.imager import pack_image, push_image, replace_dir_contents
from wield_services.wield.deploy import util as u


def whisperer_image(force_last=True, push=False):

    # TODO tag from git commit in case its not dev
    tag = 'dev'

    project_root = u.get_project_root()
    conf = u.get_conf_context_project(project_root=project_root)
    image_root = u.get_project_image_root()

    pack_image(
        conf,
        name='py37',
        image_root=image_root,
        push=False,
        force=False,
        tag=tag
    )

    pack_image(
        conf,
        name='flask',
        image_root=image_root,
        push=False,
        force=False,
        tag=tag
    )

    super_project_root = u.get_super_project_root()
    origin_path = f'{super_project_root}/micros/flask/whisperer'
    origin_regex = 'package_py.bash'

    module_root = u.get_module_root(__file__)
    image_root = f'{module_root}image'
    destination_path = f'{image_root}/whisperer'

    replace_dir_contents(
        origin_path,
        origin_regex,
        destination_path=destination_path,
        destination_dir_name='artifacts'
    )

    pack_image(
        conf,
        name='whisperer',
        image_root=image_root,
        push=False,
        force=force_last,
        tag=tag
    )

    gcp_conf = conf.providers.gcp

    if push:
        push_image(gcp_conf, name='whisperer', group='wielder', tag=tag)


if __name__ == "__main__":

    whisperer_image(push=False)

    whisperer_image(push=True, force_last=False)

