# coding=utf-8
# !/usr/bin/env python3

from common.aspect import DataAspect


class Adaptor(DataAspect):

    def __init__(self):
        pass

    def config(self):
        raise NotImplementedError("Subclass must implement config function")

    def _adapt(self, data, config):
        if callable(config):
            return config(data)

        is_tuple = isinstance(data, tuple)
        if isinstance(data, dict):
            for k, v in data.items():
                key = k if k in config else "*"
                if key in config:
                    data[k] = self._adapt(v, config[key])

        elif isinstance(data, (tuple, list)):
            data = list(data)

            for key, value in config.items():
                status, rang = self.extract_range(key, len(data))

                if not status:
                    continue
                start, end = rang
                data[start:end] = [self._adapt(a, value) for a in data[start:end]]

        return tuple(data) if is_tuple else data

    def adapt(self, data):
        return self._adapt(data, self.config())
