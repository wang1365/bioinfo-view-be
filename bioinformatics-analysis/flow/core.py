import docker
from docker.errors import DockerException

G_CLIENT = None
try:
    G_CLIENT = docker.DockerClient(base_url='unix://var/run/docker.sock')
except DockerException as e:
    print(e)


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
