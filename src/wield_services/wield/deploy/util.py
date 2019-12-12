#!/usr/bin/env python

from wielder.util.arguer import get_kube_parser
from wielder.wield.wield_project import get_conf_context_project
from wielder.wield.wield_service import get_module_root
from wielder.wield.wielder_project_locale import Locale


RUNTIME_ENV = 'RUNTIME_ENV'


def get_super_project_root():

    super_project_root = get_project_root()

    for i in range(5):
        super_project_root = super_project_root[:super_project_root.rfind('/')]

    return super_project_root


def get_project_root():

    return get_module_root(__file__)


def get_project_image_root():

    module_root = get_module_root(__file__)[:-1]

    image_root = module_root[:module_root.rfind('/') + 1] + 'image'

    return image_root


def get_project_deploy_root():

    module_root = get_module_root(__file__)[:-1]

    image_root = module_root[:module_root.rfind('/') + 1] + 'deploy'

    return image_root


def get_locale(__file__1):

    module_root = get_module_root(__file__1)
    print(f"Module root: {module_root}")

    project_root = get_project_root()
    super_project_root = get_super_project_root()
    datastores_root = project_root.replace('wield_services/wield', 'datastores')

    locale = Locale(
        project_root=project_root,
        super_project_root=super_project_root,
        module_root=module_root,
        code_path=None,
        datastores_root=datastores_root
    )

    return locale


def get_module_locale(module_name):

    project_root = get_project_root()
    super_project_root = get_super_project_root()

    deploy_root = get_project_deploy_root()

    module_root = f'{deploy_root}/{module_name}/'
    print(f"Module root: {module_root}")

    locale = Locale(
        project_root=project_root,
        super_project_root=super_project_root,
        module_root=module_root,
        code_path=None
    )

    return locale


def test():

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    runtime_env = kube_args.runtime_env

    project_root = get_project_root()
    get_conf_context_project(
        project_root=project_root,
        runtime_env=runtime_env
    )


if __name__ == "__main__":

    get_module_locale('slate')

    get_super_project_root()

    test()

