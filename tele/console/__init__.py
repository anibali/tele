from tele.meter import ValueMeter, TimeMeter, MeanValueMeter, MedianValueMeter
import tele.console.views


def _default_write_fn(step_num, rendered):
    print('[{:4d}] '.format(step_num) + ', '.join(rendered))


class Sink(tele.Sink):
    def __init__(self, cell_list, write_fn=None):
        super().__init__(cell_list)
        if write_fn is None:
            self._write_fn = _default_write_fn
        else:
            self._write_fn = write_fn

    def write(self, step_num, rendered):
        self._write_fn(step_num, rendered)


class Conf(tele.Conf):
    def __init__(self, write_fn=None):
        super().__init__()
        self._write_fn = write_fn

    def make_auto_view(self, meter_name, meter):
        if isinstance(meter, MeanValueMeter) \
                or isinstance(meter, MedianValueMeter) \
                or isinstance(meter, TimeMeter) \
                or isinstance(meter, ValueMeter):
            return tele.console.views.KeyValue([meter_name])
        return None

    def build(self, view_list):
        cell_list = [view.build() for view in view_list]
        return Sink(cell_list, self._write_fn)
