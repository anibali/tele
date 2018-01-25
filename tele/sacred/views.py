import tele
from collections import Iterable


class _ScalarCell(tele.Cell):
    def __init__(self, meter_names, run):
        super().__init__(meter_names)
        self.run = run

    def render(self, step_num, meters):
        for meter_name, meter in zip(self.meter_names, meters):
            value = meter.value()
            if isinstance(value, Iterable):
                value = next(iter(value))
            self.run.log_scalar(meter_name, value)


class Scalar(tele.View):
    def __init__(self, meter_names):
        super().__init__(meter_names)

    def build(self, run):
        return _ScalarCell(self.meter_names, run)
