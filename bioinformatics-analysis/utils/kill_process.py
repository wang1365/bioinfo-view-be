import signal
import psutil
import os

def kill(ppid, signal=signal.SIGTERM):
    try:
      process = psutil.Process(ppid)
    except psutil.NoSuchProcess:
      return
    pids = process.children(recursive=True)
    for pid in pids:
      os.kill(pid.pid, signal)