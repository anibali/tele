import tele, tele.meter
from io import StringIO, BytesIO
import base64
from PIL import Image
import torchnet.meter
import torchvision.transforms as transforms

Sink = tele.output.Sink

class Conf(tele.output.Conf):
  def __init__(self, notebook):
    super().__init__()
    self.notebook = notebook

  def make_auto_cell(self, meter_name, meter):
    if isinstance(meter, tele.meter.StringBuilderMeter):
      return TextCell(meter_name)
    if isinstance(meter, torchnet.meter.AverageValueMeter)\
    or isinstance(meter, torchnet.meter.TimeMeter):
      return LineGraphCell(meter_name)
    return None

  def _calc_frame_bounds(self, index):
    cell_width = 480
    cell_height = 308
    cell_rows = 3
    cell_cols = 4

    r, c = divmod(index, cell_cols)

    return {
      'x': c * cell_width,
      'y': r * cell_height,
      'width': cell_width,
      'height': cell_height
    }

  def build(self, cell_list):
    for i, (meter_names, cell) in enumerate(cell_list):
      bounds = self._calc_frame_bounds(i)
      frame = self.notebook.new_frame(cell.name, bounds)
      cell.set_frame(frame)
    return Sink(cell_list)

class ShowoffCell(tele.output.Cell):
  def __init__(self, name):
    super().__init__()
    self.name = name
    self.frame = None

  def set_frame(self, frame):
    self.frame = frame

class LineGraphCell(ShowoffCell):
  def __init__(self, name):
    super().__init__(name)
    self.xs = []
    self.yss = None

  def render(self, step_num, meters):
    if self.yss is None:
      self.yss = [[] for _ in meters]
    self.xs.append(step_num)
    series_names = []
    for i, (meter_name, meter) in enumerate(meters.items()):
      value = meter.value()
      if isinstance(meter, torchnet.meter.AverageValueMeter):
        value = value[0]
      self.yss[i].append(value)
      series_names.append(meter_name)
    self.frame.line_graph(self.xs, self.yss, series_names=series_names)

class TextCell(ShowoffCell):
  def __init__(self, name):
    super().__init__(name)

  def render(self, step_num, meters):
    meter_name, meter = next(iter(meters.items()))
    self.frame.text(str(meter.value()))

class ImageCell(ShowoffCell):
  def __init__(self, name, images_per_row=None):
    super().__init__(name)
    self.images_per_row = images_per_row

  def render(self, step_num, meters):
    images = []
    for meter_name, meter in meters.items():
      value = meter.value()
      if isinstance(value, list):
        images.extend(value)
      else:
        images.append(value)

    if self.images_per_row is None:
      img_tag_template = '<img src=data:image/png;base64,{}>'
    else:
      width = '{:0.2f}%'.format(100 / self.images_per_row)
      img_tag_template = '<img style="width: ' + width + ';" src=data:image/png;base64,{}>'

    stream = StringIO()
    stream.write('<div>')
    for img in images:
      if not isinstance(img, Image.Image):
        img = transforms.ToPILImage()(value.cpu())
      buf = BytesIO()
      img.save(buf, format='PNG')
      b64_str = base64.b64encode(buf.getvalue()).decode('utf-8')
      stream.write(img_tag_template.format(b64_str))
    stream.write('</div>')
    self.frame.html(stream.getvalue())

class GraphvizCell(ShowoffCell):
  def __init__(self, name):
    super().__init__(name)

  def render(self, step_num, meters):
    meter_name, meter = next(iter(meters.items()))
    value = meter.value()
    svg_bytes = value.pipe(format='svg')
    b64_str = base64.b64encode(svg_bytes).decode('utf-8')
    img_tag_template = '<img style="width: 100%;" src=data:image/svg+xml;base64,{}>'
    self.frame.html(img_tag_template.format(b64_str))

class InspectValueCell(ShowoffCell):
  def __init__(self, name, flatten=False):
    super().__init__(name)
    self.flatten = flatten

  def render(self, step_num, meters):
    items = []
    for meter_name, meter in meters.items():
      value = meter.value()
      if self.flatten and hasattr(value, 'items'):
        for k, v in value.items():
          key = meter_name + '.' + k
          str_value = str(v)
          items.append((key, str_value))
      else:
        key = meter_name
        str_value = str(value)
        items.append((key, str_value))

    stream = StringIO()
    stream.write('<table style="width: 100%; table-layout: fixed;">')
    for key, str_value in items:
      stream.write('<tr><td>')
      stream.write(key)
      stream.write('</td></tr><tr><td><pre>')
      stream.write(str_value)
      stream.write('</pre></td></tr>')
    stream.write('</table>')
    self.frame.html(stream.getvalue())
