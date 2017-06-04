from tele import Telemetry
from tele.meter import ValueMeter
from tele.output import showoff
import unittest
from tempfile import TemporaryDirectory
import os
import json
import pyshowoff

class DummyClient(pyshowoff.Client):
  def __init__(self, callback=None):
    super().__init__('dummy:1337', True)
    self.callback = callback

  def request(self, method, path, data=None):
    if self.callback:
      return self.callback(method, path, data)
    return None

class TestShowoffOutput(unittest.TestCase):
  def test_normal(self):
    patch_data = {}
    def callback(method, path, data):
      if method.lower() == 'post' and path == '/api/v2/frames':
        return {'data': {'id': '100'}}
      if method.lower() == 'patch' and path == '/api/v2/frames/100':
        patch_data.clear()
        patch_data.update(data)
        return None
      self.fail('unexpected Showoff request')
    client = DummyClient(callback)
    notebook = pyshowoff.Notebook(client, 1)
    t = Telemetry({'val': ValueMeter()})
    t['val'].set_value(42)
    t.sink(showoff.Conf(notebook), [(['val'], showoff.TextCell('Value'))])
    t.step()
    self.assertEqual(patch_data, {'data': {
      'id': '100',
      'type': 'frames',
      'attributes': {'type': 'text', 'content': {'body': '42'}}
    }})
