import psutil


class SystemMemory:
    def __init__(self):
        self.mem = psutil.virtual_memory()

    @property
    def totol_memory(self):
        return float(self.mem.total) / 1024 / 1024

    @property
    def used_memory(self):
        return float(self.mem.used) / 1024 / 1024

    @property
    def free_memory(self):
        return float(self.mem.free) / 1024 / 1024
