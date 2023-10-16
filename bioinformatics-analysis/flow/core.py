import logging

import docker
from docker.errors import DockerException

G_CLIENT = None
try:
    G_CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock', timeout=60 * 10)
    print('create docker client success', G_CLIENT)
    logging.getLogger().warning('create docker client success', G_CLIENT)
except DockerException as e:
    print('!!!create docker client failed', e)
    logging.getLogger().warning('create docker client failed', e)


def has_image(image_name):
    try:
        G_CLIENT.images.get(image_name)
        return True
    except docker.errors.ImageNotFound:
        return False
    except Exception as e:
        print(e)


def load_image(tar_path, image_name):
    try:
        if has_image(image_name):
            return

        with open(tar_path, "rb") as fp:
            G_CLIENT.images.load(fp)
    except Exception as e:
        print(e)
        raise Exception("Load Image Error")
