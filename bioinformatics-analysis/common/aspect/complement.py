from common.aspect import DataAspect


class Complement(DataAspect):

    def __init__(self):
        self.meta_types = (int, float, str)

    def config(self):
        raise NotImplementedError("Subclass must implement config function")

    def _do_complete(self, func_or_default, data, path, **args):
        if callable(func_or_default):
            return func_or_default(data, path=path, origin_data=self._origin_data, **args)
        return func_or_default if data == {} else data

    def _complete(self, data, config, path, **args):
        if callable(config) or isinstance(config, self.meta_types):
            return self._do_complete(config, data, path, **args)

        is_tuple = isinstance(data, tuple)
        if isinstance(data, (tuple, list)):
            data = list(data)

            for key, value in config.items():
                status, rang = self.extract_range(key, len(data))
                if not status:
                    continue
                start, end = rang

                for i, a in enumerate(data[start:end]):
                    data[start + i] = self._complete(a, value, path + [start + i], **args)

        elif isinstance(config, dict):
            for key, value in config.items():
                if key == '*':
                    for k, v in data.items():
                        data[k] = self._complete(v, value, path + [k], **args)

                else:
                    if key not in data:
                        data[key] = {}
                    data[key] = self._complete(data[key], config[key], path + [key], **args)

        return tuple(data) if is_tuple else data

    def complete(self, data, **args):
        self._origin_data = data
        return self._complete(data, self.config(), [], **args)
