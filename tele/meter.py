from io import StringIO
import numpy as np
from scipy.stats import norm
from math import sqrt
from time import perf_counter


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


class MaxValueMeter(Meter):
    def __init__(self, skip_reset=False):
        self._value = None
        super().__init__(skip_reset)

    def add(self, new_value):
        if self._value is not None and new_value <= self._value:
            return False

        self._value = new_value
        return True

    def reset(self):
        self._value = None

    def value(self):
        return self._value


class SumMeter(Meter):
    def __init__(self, initial_value=0, skip_reset=False):
        self.initial_value = initial_value
        self._value = None
        super().__init__(skip_reset)

    def add(self, value):
        self._value += value

    def value(self):
        return self._value

    def reset(self):
        self._value = self.initial_value


class MeanValueMeter(Meter):
    def __init__(self, skip_reset=False):
        super().__init__(skip_reset)

    def add(self, value, n=1):
        self.sum += value
        self.variance += value ** 2
        self.n += n

        if self.n == 0:
            self.mean = np.nan
            self.stddev = np.nan
            return

        self.mean = self.sum / self.n

        if self.n == 1:
            self.stddev = np.inf
            return

        self.stddev = sqrt((self.variance - self.n * self.mean ** 2) / (self.n - 1))

    def value(self):
        return self.mean, self.stddev

    def reset(self):
        self.n = 0
        self.sum = 0
        self.variance = 0
        self.mean = np.nan
        self.stddev = np.nan


class MedianValueMeter(Meter):
    def __init__(self, skip_reset=False):
        self.values = []
        super().__init__(skip_reset)

    def add(self, value):
        self.values.append(value)

    def value(self):
        data = np.asarray(self.values)

        median = np.median(data)

        # Calculate median absolute deviation (assumes data is normally distributed)
        k = norm.ppf(0.75)
        mad = np.median(np.fabs(data - median) / k)

        return median, mad

    def reset(self):
        self.values.clear()


class TimeMeter(Meter):
    def __init__(self, skip_reset=False):
        super().__init__(skip_reset)

    def value(self):
        return perf_counter() - self.time

    def reset(self):
        self.time = perf_counter()
