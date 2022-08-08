class DataAspect:

    def value_by_path(self, data, path, default=None):
        if len(path) <= 0:
            return data

        key = path[0]
        if isinstance(data, dict):
            if key in data:
                return self.value_by_path(data[key], path[1:], default=default)
        elif isinstance(data, (list, tuple)):
            if -len(data) <= key < len(data):
                return self.value_by_path(data[key], path[1:], default=default)

        return default

    def extract_range(self, key, length):
        index = None
        tp, start, end = None, None, None

        if len(key) == 1:
            tp = key[0]
            index = 0
        elif len(key) == 2:
            tp, index = key
        elif len(key) == 3:
            tp, start, end = key

        if tp != 'list':
            return False, None

        if isinstance(index, int):
            start, end = index, length + 1
        elif isinstance(index, tuple):
            if len(index) == 1:
                start, end = index[0], length + 1
            elif len(index) == 2:
                start, end = index
        if start is None or end is None:
            return False, None

        return True, (start, end)
