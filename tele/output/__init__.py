from collections import OrderedDict
from io import StringIO

class Sink():
  def __init__(self, cell_list):
    self.cell_list = cell_list
    self.cell_index = {}

    for meter_names, cell in cell_list:
      for meter_name in meter_names:
        if meter_name in self.cell_index:
          meter_cells = self.cell_index[meter_name]
        else:
          meter_cells = []
          self.cell_index[meter_name] = meter_cells
        meter_cells.append(cell)

  def render_all(self, step_num, meters):
    render_results = []
    for i, (meter_names, cell) in enumerate(self.cell_list):
      cell_meters = OrderedDict([(mn, meters[mn]) for mn in meter_names])
      render_results.append(cell.render(step_num, cell_meters))
    return render_results

class Conf():
  def make_auto_cell(self, meter_name, meter):
    return None

  def build(self, cell_list):
    raise NotImplementedError()

class Cell():
  def render(self, step_num, meters):
    raise 'not implemented'
