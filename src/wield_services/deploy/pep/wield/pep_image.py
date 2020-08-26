#!/usr/bin/env python

import logging
import os
from enum import Enum
from shutil import rmtree, copyfile

from wield_services.wield.deploy.util import get_locale
from wielder.util.arguer import replace_none_vars_from_args
from wielder.util.commander import async_cmd
from wielder.util.wgit import clone_or_update

from wield_services.wield.log_util import setup_logging
from wielder.util.imager import pack_image, push_image, replace_dir_contents
from wield_services.wield.deploy import util as u
from wielder.wield.wield_service import WieldService


class ArtifactMethod(Enum):

    INIT_REPO = 'INIT_REPO'
    UPDATE_REPO = 'UPDATE_REPO'
    GET_DIR = 'GET_DIR'


def pep_image(force_last=True, push=False):

    locale = get_locale(__file__)

    action, mode, enable_debug, local_mount, service_mode = replace_none_vars_from_args(
        action=None,
        mode=None,
        enable_debug=None,
        local_mount=None,
        service_mode=None,
        project_override=None
    )

    service = WieldService(
        name='pep',
        locale=locale,
        mode=mode,
        service_mode=service_mode,
    )

    plan = service.plan.module_conf.packaging

    image_name = plan.image_name

    tag = plan.git.branch

    project_root = u.get_project_root()
    conf = u.get_conf_context_project(project_root=project_root)

    image_root = u.get_project_image_root()

    pack_image(
        conf=conf,
        name='perl',
        image_root=image_root,
        push=False,
        force=True,
        tag=tag
    )

    pack_image(
        conf=conf,
        name='perl_py',
        image_root=image_root,
        push=False,
        force=True,
        tag=tag
    )

    try:
        origin_path = plan.origin_path
        origin_regex = plan.origin_regex
    except AttributeError:
        super_project_root = u.get_super_project_root()
        origin_path = f'{super_project_root}/micros/perl/pep'
        origin_regex = 'pep.pl'

    module_root = u.get_module_root(__file__)
    image_root = f'{module_root}image'
    destination_path = f'{image_root}/{image_name}'

    artifacts_dir = f'{destination_path}/artifacts'

    artifact_method = plan.artifact_method

    if artifact_method == ArtifactMethod.GET_DIR.value or artifact_method == ArtifactMethod.INIT_REPO.value:
        rmtree(artifacts_dir, ignore_errors=True)

    if artifact_method == ArtifactMethod.GET_DIR.value:

        replace_dir_contents(
            origin_path,
            origin_regex,
            destination_path=destination_path,
            destination_dir_name='artifacts'
        )
    else:
        clone_or_update(source=origin_path, destination=artifacts_dir, branch=plan.git.branch)

        if artifact_method == ArtifactMethod.INIT_REPO.value:

            for art in plan.artifacts:

                os.makedirs(f"{artifacts_dir}/{art[0]}", exist_ok=True)

                try:
                    copyfile(src=f"{origin_path}/{art[0]}/{art[1]}", dst=f"{artifacts_dir}/{art[0]}/{art[1]}")

                except Exception as e:
                    logging.error(str(e))

            _cmd = f'{artifacts_dir}/pypep/prepare.bash'

            a = async_cmd(_cmd)

            for b in a:
                print(b)

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

    pep_image(push=False)

    # pep_image(force_last=False, push=True)

