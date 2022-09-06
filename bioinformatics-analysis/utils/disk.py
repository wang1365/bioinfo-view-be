import subprocess
import os

from account.models import Account


def cal_dir_size(dirctory, user_id):
    if not os.path.exists(dirctory):
        return
    res = subprocess.Popen(
        f'du -sh {dirctory}',
        shell=True,
        stdout=subprocess.PIPE,
        encoding='utf8')
    size = res.stdout.read().split("\t")[0]
    if size[-1] == "G":
        size = int(size[:-1]) * 1024
    elif size[-1] == "T":
        size = int(size[:-1]) * 1024 * 1024
    elif size[-1] == "M":
        size = int(size[:-1])
    elif size[-1] == "K":
        size = int(size[:-1]) / 1024
    elif size[-1] == "B":
        size = int(size[:-1]) / (1024 * 1024)
    Account.objects.filter(pk=user_id).update(used_disk=size)
