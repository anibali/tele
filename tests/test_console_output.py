from tele import Telemetry
from tele.meter import ValueMeter
from tele.output import console
import unittest

from common import captured_output

class TestConsoleOutput(unittest.TestCase):
  def test_normal(self):
    t = Telemetry({'val': ValueMeter()})
    t['val'].set_value(42)
    t.sink(console.Conf(), [(['val'], console.TextCell())])
    with captured_output() as (out, err):
      t.step()
      self.assertEqual(out.getvalue().strip(), '[   0] val=42')

  def test_auto_cell(self):
    t = Telemetry({'val': ValueMeter()})
    t['val'].set_value(42)
    t.sink(console.Conf(), auto_cell=True)
    with captured_output() as (out, err):
      t.step()
      self.assertEqual(out.getvalue().strip(), '[   0] val=42')
