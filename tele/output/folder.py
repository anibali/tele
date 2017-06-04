import tele
from collections import OrderedDict
import torchnet.meter
import os
import json
import h5py

Sink = tele.output.Sink

class Conf(tele.output.Conf):
  def __init__(self, dir_path):
    super().__init__()
    self.dir_path = dir_path

  def make_auto_cell(self, meter_name, meter):
    return None

  def build(self, cell_list):
    if not os.path.exists(self.dir_path):
      os.makedirs(self.dir_path)
    for i, (meter_names, cell) in enumerate(cell_list):
      cell.set_dir(self.dir_path)
    return Sink(cell_list)

class FolderCell(tele.output.Cell):
  def __init__(self, filename_template):
    super().__init__()
    self.filename_template = filename_template
    self.dir_path = None

  def set_dir(self, dir_path):
    self.dir_path = dir_path

  def build_path(self, step_num):
    return os.path.join(self.dir_path, self.filename_template.format(step_num))

class JSONCell(FolderCell):
  def __init__(self, filename_template='metrics_{:04d}.json'):
    super().__init__(filename_template)

  def render(self, step_num, meters):
    path = self.build_path(step_num)
    values = {}
    for meter_name, meter in meters.items():
      values[meter_name] = meter.value()
    with open(path, 'w') as f:
      json.dump(values, f)

class GrowingJSONCell(FolderCell):
  def __init__(self, filename_template='saved_metrics.json'):
    super().__init__(filename_template)

  def render(self, step_num, meters):
    file_path = self.build_path(step_num)
    if os.path.isfile(file_path):
      with open(file_path, 'r') as f:
        values = json.load(f)
    else:
      values = {}
    for meter_name, meter in meters.items():
      if not meter_name in values:
        values[meter_name] = []
      values[meter_name].append(meter.value())
    with open(file_path, 'w') as f:
      json.dump(values, f)

class HDF5Cell(FolderCell):
  def __init__(self, filename_template='data_{:04d}.h5', path_map={}):
    super().__init__(filename_template)
    self.path_map = path_map

  def render(self, step_num, meters):
    file_path = self.build_path(step_num)
    with h5py.File(file_path, 'w') as f:
      for meter_name, meter in meters.items():
        if meter_name in self.path_map:
          h5_path = self.path_map[meter_name]
        else:
          h5_path = meter_name
        f.create_dataset(h5_path, data=meter.value())
