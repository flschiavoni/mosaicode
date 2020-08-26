import unittest
from mosaicomponents.charfield import CharField

class TestCharField(unittest.TestCase):

    def setUp(self):
        CharField(None, None)
        self.field = CharField({"label": "test", "value": "False"}, None)
        self.field = CharField({"label": "test", "value": "True"}, None)
        self.field = CharField({}, self.test_value)

    def test_value(self):
        value1 = 'a'
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')
        value1 = 'b'
        self.field.set_value(value1)
        value2 = self.field.get_value()
        self.assertEqual(value1, value2, 'incorrect value')

