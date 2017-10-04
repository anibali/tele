from io import StringIO


class Meter:
    def __init__(self, skip_reset):
        self.reset()
        self.skip_reset = skip_reset

    def reset(self):
        pass

    def value(self):
        return None


class ValueMeter(Meter):
    def __init__(self, skip_reset=False):
        self._value = None
        super().__init__(skip_reset)

    def set_value(self, value):
        self._value = value

    def reset(self):
        self._value = None

    def value(self):
        return self._value


class ListMeter(Meter):
    def __init__(self, skip_reset=False):
        self._list = None
        super().__init__(skip_reset)

    def add(self, value):
        self._list.append(value)

    def add_all(self, values):
        self._list.extend(values)

    def reset(self):
        self._list = []

    def value(self):
        return self._list


class StringBuilderMeter(Meter):
    def __init__(self, skip_reset=False):
        self._value = None
        super().__init__(skip_reset)

    def add(self, part):
        self._value.write(part)

    def add_line(self, line):
        self.add(line)
        self.add('\n')

    def reset(self):
        self._value = StringIO()

    def value(self):
        return self._value.getvalue()
