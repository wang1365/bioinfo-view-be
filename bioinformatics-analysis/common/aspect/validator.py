#!/usr/bin/env python3
# encoding: utf-8

import json
import logging
import traceback
from collections import OrderedDict

from common.aspect import DataAspect
from common.consts.consts import Environment
from service.larkbot import LarkBot


class Validator(DataAspect):

    def __init__(self, send_lark=True):
        self.send_lark = send_lark

    def is_int(self, value, **params):
        return isinstance(value, int)

    def is_string(self, value, **params):
        return isinstance(value, str)

    def is_list(self, value, **params):
        return isinstance(value, list)

    def is_dict(self, value, **params):
        return isinstance(value, dict)

    def is_number(self, value, **params):
        return isinstance(value, (int, float))

    def config(self):
        raise NotImplementedError("Subclass must implement config function")

    def _check_validate(self, config, data, path):
        funcs = [config]
        if isinstance(config, tuple):
            funcs = config

        for func in funcs:
            if not func(data, path=path, origin_data=self._origin_data):
                raise ValueError(
                    "key {} not statisfied func: {}".format(str(path),
                                                            func.__name__))

        return True

    def _validate(self, data, config, path):
        if callable(config) or isinstance(config, tuple):
            return self._check_validate(config, data, path)

        if isinstance(data, dict):
            if '_required_' in config:
                required_keys = config['_required_']
                for k in required_keys:
                    if k not in data:
                        raise ValueError(
                            "key {} not exists".format(str(path + [k])))

            for k, v in data.items():
                key = k if k in config else "*"
                if key in config:
                    self._validate(v, config[key], path + [k])

        elif isinstance(data, (tuple, list)):
            data = list(data)

            for key, value in config.items():
                status, rang = self.extract_range(key, len(data))
                if not status:
                    continue
                start, end = rang

                for i, a in enumerate(data[start:end]):
                    self._validate(a, value, path + [start + i])

    def validate(self, data):
        self._origin_data = data
        try:
            self._validate(data, self.config(), [])
            return True
        except ValueError as e:
            logging.error(json.dumps(data))
            logging.error(e)
            logging.error(traceback.format_exc())
            if self.send_lark:
                LarkBot(environment=Environment.CronJob).send_format_msg(
                    title='数据校验错误',
                    msg_dict=OrderedDict([('message', str(e))])
                )
            return False
