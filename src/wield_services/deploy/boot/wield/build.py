#!/usr/bin/env python
import logging
import os
from shutil import copyfile

from wield_services.wield.log_util import setup_logging
from wielder.util.commander import async_cmd, subprocess_cmd
from wield_services.wield.deploy import util as u
from wielder.util.util import DirContext


def build_for_container_mount(force_last=True, push=False):

    project_root = u.get_project_root()

    conf = u.get_conf_context_project(project_root=project_root)

    super_project_root = u.get_super_project_root()
    # TODO get the suffix from module config
    origin_path = f'{super_project_root}/micros/boot/eve'

    with DirContext(origin_path):

        subprocess_cmd(f'./gradlew build')

    jar_dir = f'{origin_path}/build/libs'

    origin_regex = 'eve*.jar'

    target_jar = async_cmd(f"find {jar_dir} -name {origin_regex}")[0][:-1]

    old_name = target_jar.split('/')[-1]

    copyfile(f'{jar_dir}/{old_name}', f'{jar_dir}/app.jar')


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)

    logging.debug('break point')

    build_for_container_mount(push=False)

