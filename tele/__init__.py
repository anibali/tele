class Telemetry():
  def __init__(self, meters):
    self.meters = meters
    self.sinks = []
    self.step_num = 0

  def sink(self, conf, cell_list=[], auto_cell=False):
    if auto_cell:
      meters_with_cells = []
      for meter_names, cell in cell_list:
        meters_with_cells.extend(meter_names)
      meters_without_cells = set(self.meters.keys()) - set(meters_with_cells)
      for meter_name in sorted(meters_without_cells):
        cell = conf.make_auto_cell(meter_name, self.meters[meter_name])
        if cell is not None:
          cell_list.append(([meter_name], cell))
    sink = conf.build(cell_list)
    self.sinks.append(sink)
    return sink

  def step(self):
    for sink in self.sinks:
      sink.render_all(self.step_num, self.meters)
    for meter_name, meter in self.meters.items():
      if not hasattr(meter, 'skip_reset') or not meter.skip_reset:
        meter.reset()
    self.step_num += 1

  def __getitem__(self, meter_name):
    return self.meters[meter_name]
