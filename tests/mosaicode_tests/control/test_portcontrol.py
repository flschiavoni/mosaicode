from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.portcontrol import PortControl
from mosaicode.system import System

class TestPortControl(TestBase):

    def test_add_port(self):
        PortControl()
        port = self.create_port()
        PortControl.delete_port(port.type)
        System()
        PortControl.add_port(self.create_port())
        System.reload()
        PortControl.delete_port(port.type)
        System.add_port(port)
        PortControl.delete_port(port.type)

    def test_export_xml(self):
        PortControl.export_xml()
        PortControl.load("test.xml")
        PortControl.print_port(self.create_port())

