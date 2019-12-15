#!/usr/bin/env python
import logging
import os

from wield_services.wield.log_util import setup_logging
from wielder.util.imager import pack_image, push_image, replace_dir_contents
from wield_services.wield.deploy import util as u

ARTIFACT_DIR = 'artifacts'


def boot_image(force_last=True, push=False):

    # TODO tag from git commit in case its not dev
    image_name = 'boot'

    tag = 'dev'

    project_root = u.get_project_root()
    conf = u.get_conf_context_project(project_root=project_root)

    pack_image(
        conf=conf,
        name='py_base',
        image_root=u.get_project_image_root(),
        push=False,
        force=False,
        tag=tag
    )

    pack_image(
        conf=conf,
        name='j11_py',
        image_root=u.get_project_image_root(),
        push=False,
        force=False,
        tag=tag
    )

    super_project_root = u.get_super_project_root()
    # TODO get the suffix from module config
    origin_path = f'{super_project_root}/micros/boot/eve/build/libs'
    origin_regex = 'eve*.jar'
    #
    module_root = u.get_module_root(__file__)
    image_root = f'{module_root}image'
    destination_path = f'{image_root}/{image_name}'

    # TODO compile conditional on cli or config ( ./gradlew build && java -jar build/libs/eve-0.1.0.jar)
    origin_jar = replace_dir_contents(
        origin_path,
        origin_regex,
        destination_path=destination_path,
        destination_dir_name=ARTIFACT_DIR
    )

    old_name = origin_jar.split('/')[-1]

    os.rename(f'{destination_path}/{ARTIFACT_DIR}/{old_name}', f'{destination_path}/{ARTIFACT_DIR}/app.jar')

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

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    boot_image(push=False)

    # slate_image(force_last=False, push=True)

