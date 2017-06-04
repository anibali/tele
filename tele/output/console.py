import tele
import torchnet.meter

class Sink(tele.output.Sink):
  def render_all(self, step_num, meters):
    render_results = super().render_all(step_num, meters)
    print('[{:4d}] '.format(step_num) + ', '.join(render_results))
    return render_results

class Conf(tele.output.Conf):
  def make_auto_cell(self, meter_name, meter):
    if isinstance(meter, torchnet.meter.AverageValueMeter)\
    or isinstance(meter, torchnet.meter.TimeMeter)\
    or isinstance(meter, tele.meter.ValueMeter):
      return TextCell()
    return None

  def build(self, cell_list):
    return Sink(cell_list)

class TextCell(tele.output.Cell):
  def __init__(self):
    super().__init__()

  def render(self, step_num, meters):
    meter_name, meter = next(iter(meters.items()))
    value = meter.value()
    if isinstance(meter, torchnet.meter.AverageValueMeter):
      (mean, std) = value
      value_str = u'{:0.4f}\u00b1{:0.4f}'.format(mean, std)
    elif isinstance(value, float):
      value_str = '{:0.4f}'.format(value)
    else:
      value_str = str(value)
    return '='.join([meter_name, value_str])
