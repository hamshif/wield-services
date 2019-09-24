#!/usr/bin/env python

from wielder.util.imager import pack_image, push_image, replace_dir_contents
from wield_services.wield.deploy import util as u


def pep_image(force_last=True, push=False):

    # TODO tag from git commit in case its not dev
    image_name = 'pep'

    tag = 'dev'

    project_root = u.get_project_root()
    conf = u.get_conf_context_project(project_root=project_root)

    pack_image(
        conf=conf,
        name='perl',
        image_root=u.get_project_image_root(),
        push=False,
        force=True,
        tag=tag
    )

    pack_image(
        conf=conf,
        name='perl_py',
        image_root=u.get_project_image_root(),
        push=False,
        force=True,
        tag=tag
    )

    super_project_root = u.get_super_project_root()
    origin_path = f'{super_project_root}/micros/perl/pep'
    origin_regex = 'pep.pl'

    module_root = u.get_module_root(__file__)
    image_root = f'{module_root}image'
    destination_path = f'{image_root}/{image_name}'

    replace_dir_contents(
        origin_path,
        origin_regex,
        destination_path=destination_path,
        destination_dir_name='artifacts'
    )

    pack_image(
        conf,
        name=image_name,
        image_root=image_root,
        push=False,
        force=force_last,
        tag=tag
    )

    gcp_conf = conf.providers.gcp

    if push:
        push_image(gcp_conf, name=image_name, group='wielder', tag=tag)


if __name__ == "__main__":

    pep_image(push=False)

    # slate_image(force_last=False, push=True)

