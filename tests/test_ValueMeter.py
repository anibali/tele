from tele.meter import ValueMeter
import unittest

class TestValueMeter(unittest.TestCase):
  def test_set_value(self):
    meter = ValueMeter()
    self.assertIsNone(meter.value())
    meter.set_value(42)
    self.assertEqual(42, meter.value())
