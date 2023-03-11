import subprocess
import os
import time

from account.models import Account


def cal_dir_size(dirctory, user_id):
    if not os.path.exists(dirctory):
        return
    time.sleep(3)
    size = dir_size(dirctory)
    Account.objects.filter(pk=user_id).update(used_disk=size)


def dir_size(dirctory):
    if not os.path.exists(dirctory):
        return 0
    res = subprocess.Popen(
        f'du -sh {dirctory}',
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf8')
    size = res.stdout.read().split("\t")[0]
    if size[-1] == "G":
        size = float(size[:-1]) * 1024
    elif size[-1] == "T":
        size = float(size[:-1]) * 1024 * 1024
    elif size[-1] == "M":
        size = float(size[:-1])
    elif size[-1] == "K":
        size = float(size[:-1]) / 1024
    elif size[-1] == "B":
        size = float(size[:-1]) / (1024 * 1024)
    return size