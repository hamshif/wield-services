#!/usr/bin/env python

from wielder.util.imager import pack_image, replace_dir_contents
from wield_services.wield.deploy import util as U


def whisperer_image():

    # TODO tag from git commit in case its not dev
    tag='dev'

    project_root = U.get_project_root()
    conf = U.get_conf_context_project(project_root=project_root)
    image_root = U.get_project_image_root()

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

    super_project_root = U.get_super_project_root()
    origin_path = f'{super_project_root}/micros/flask/whisperer'
    origin_regex = 'package_py.bash'

    module_root = U.get_module_root(__file__)
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
        force=True,
        tag=tag
    )

    # push_image(conf)


if __name__ == "__main__":

    whisperer_image()
