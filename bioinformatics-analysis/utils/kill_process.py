import signal
import psutil
import os
from flow.core import G_CLIENT


def kill(ppid, signal=signal.SIGTERM):
    try:
        process = psutil.Process(ppid)
    except psutil.NoSuchProcess:
        return
    pids = process.children(recursive=True)
    for pid in pids:
        os.kill(pid.pid, signal)


def stop_docker(container_id):
    container = G_CLIENT.containers.get(container_id)
    try:
        container.kill()
        container.remove()
    except Exception as e:
        print(f"stop docker error, container_id: {container_id}, error: {e}")
