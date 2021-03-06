import tele
from tele.meter import StringBuilderMeter, TimeMeter, MeanValueMeter
import tele.showoff.views

Sink = tele.Sink


class Conf(tele.Conf):
    def __init__(self, notebook):
        super().__init__()
        self.notebook = notebook

    def make_auto_view(self, meter_name, meter):
        if isinstance(meter, StringBuilderMeter):
            return tele.showoff.views.Text(meter_name)
        if isinstance(meter, MeanValueMeter) \
                or isinstance(meter, TimeMeter):
            return tele.showoff.views.LineGraph(meter_name)
        return None

    @staticmethod
    def _calc_frame_bounds(index):
        cell_width = 478
        cell_height = 308
        cell_cols = 4

        r, c = divmod(index, cell_cols)

        return {
            'x': c * cell_width,
            'y': r * cell_height,
            'width': cell_width,
            'height': cell_height
        }

    def build(self, view_list):
        cell_list = []
        for i, view in enumerate(view_list):
            bounds = self._calc_frame_bounds(i)
            cell = view.build(self.notebook.add_frame(view.frame_title, bounds).result())
            cell_list.append(cell)
        return Sink(cell_list)
