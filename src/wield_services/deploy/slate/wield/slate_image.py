#!/usr/bin/env python
import os
from shutil import copyfile

from wielder.util.arguer import get_kube_parser
from wielder.util.commander import async_cmd
from wielder.util.imager import replace_file

from wield_kube.wield.conf.rtp_conf import local_process_args


def push_image(conf):

    use_minikube_repo = ''

    if conf.kube_context == "minikube":

        use_minikube_repo = "eval $(minikube docker-env); "

    os.system(f"{use_minikube_repo} "
              f'gcloud docker -- push {conf.gcp_image_repo_zone}/{conf.gcp_project}/slate:latest;'
              f'gcloud container images list --repository={conf.gcp_image_repo_zone}/{conf.gcp_project}/rtp/slate;')


def pack_image(conf, push=False, force_base=False):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    print(f"current working dir: {dir_path}")
    module_root = dir_path[:dir_path.rfind('/') + 1]
    print(f"Module root: {module_root}")

    use_minikube_repo = ''

    if conf.kube_context == "minikube":

        use_minikube_repo = "eval $(minikube docker-env); "

    base_image_trace = async_cmd(
        f"{use_minikube_repo}"
        f"$(docker images | grep slate | grep base);"
    )

    print(f"base_image_trace: {base_image_trace}")

    # Check if the list is empty
    if force_base or not base_image_trace:

        print(f"attempting to create base image")

        os.system(f"{use_minikube_repo}"
                  f"docker build -t slate/base:dev {module_root}image/base;"
                  f'echo "These are the resulting images:";'
                  f"docker images | grep slate | grep base;")

    # TODO add an error report and exit after failure in base
    os.system(f"{use_minikube_repo}"
              f"docker build -t slate:dev {module_root}image;"
              f"docker tag slate:dev {conf.gcp_image_repo_zone}/{conf.gcp_project}/slate:latest;"
              f'echo "These are the resulting images:";'
              f"docker images | grep slate;")

    if push:
        push_image(conf)


if __name__ == "__main__":

    kube_parser = get_kube_parser()
    kube_args = kube_parser.parse_args()

    _conf = local_process_args(kube_args)
    # TODO add tag
    pack_image(_conf, push=False, force_base=False)

    # push_image(conf)
