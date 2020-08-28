from tests.mosaicode_tests.test_base import TestBase
from mosaicode.system import System

class TestSystem(TestBase):

    def test_get_dir_name(self):
        System()
        System.get_dir_name(self.create_diagram())

    def test_constructor(self):
        System()
        System.instance = None
        System()

    def test_log(self):
        System.log("Message")
        System.log(None)

    def test_set_log(self):
        System.set_log(None)
        System.instance = None
        System.set_log(None)

    def test_remove_block(self):
        System.remove_block("None")
        System.remove_block(self.create_block())

    def test_remove_port(self):
        System.remove_port("None")
        System.remove_port(self.create_port())

    def test_get_code_templates(self):
        System.get_code_templates()

    def test_get_ports(self):
        System.get_ports()

    def test_get_preferences(self):
        System.get_preferences()

    def test_get_plugins(self):
        System.get_plugins()

    def test_get_code_templates(self):
        System.get_code_templates()

