import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
import unittest
from time import sleep
from abc import ABCMeta
from mosaicode.system import System as System
from mosaicode.GUI.block import Block
from mosaicode.GUI.comment import Comment
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.mainwindow import MainWindow
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.blockmodel import BlockModel
from mosaicode.model.port import Port
from mosaicode.model.codetemplate import CodeTemplate
from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.port import Port

class TestBase(unittest.TestCase):
    __metaclass__ = ABCMeta

    def refresh_gui(self, delay=0):
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
        sleep(delay)

    def create_main_window(self):
        return MainWindow()

    def create_diagram(self, main_window=None):
        if main_window is None:
            main_window = self.create_main_window()
        diagram = Diagram(main_window)
        diagram.language = "Test"
        diagram.zoom = 2
        diagram.code_template = self.create_code_template()
        return diagram

    def create_full_diagram(self, main_window=None):
        if main_window is None:
            main_window = self.create_main_window()
        diagram = Diagram(main_window)
        self.assertEquals(diagram.last_id, 0)
        diagram.language = "Test"
        diagram.zoom = 2
        diagram_control = self.create_diagram_control(diagram)

        block0 = self.create_block(diagram_control)
        result = diagram_control.add_block(block0)

        block1 = self.create_block(diagram_control)
        result = diagram_control.add_block(block1)
        assert result

        block2 = self.create_block(diagram_control)
        result = diagram_control.add_block(block2)
        assert result

        connection = ConnectionModel(
                    diagram,
                    block1,
                    block1.ports[0],
                    block2,
                    block2.ports[0]
                    )
        result = diagram_control.add_connection(connection)
        self.assertEquals(result[0], False)

        connection = ConnectionModel(
                    diagram,
                    block1,
                    block1.ports[1],
                    block2,
                    block2.ports[0]
                    )
        result = diagram_control.add_connection(connection)
        self.assertEquals(result[1], "Success")

        connection = ConnectionModel(
                    diagram,
                    block2,
                    block2.ports[1],
                    block1,
                    block1.ports[1]
                    )
        result = diagram_control.add_connection(connection)
        self.assertEquals(result[0], False)


        connection = ConnectionModel(
                    diagram,
                    block1,
                    block1.ports[1],
                    block1,
                    block1.ports[0]
                    )
        result = diagram_control.add_connection(connection)
        self.assertEquals(result[0], False)

        connection = ConnectionModel(diagram, None, None, None, None)
        result = diagram_control.add_connection(connection)
        self.assertEquals(result[0], False)

        comment = self.create_comment(diagram)
        diagram_control.add_comment(comment)
        comment = self.create_comment(diagram)
        diagram_control.add_comment(comment)
        diagram.code_template = self.create_code_template()
        return diagram


    def create_diagram_control(self, diagram=None):
        if diagram is None:
            diagram = self.create_diagram()
        diagram_control = DiagramControl(diagram)
        diagram_control.connectors = []
        diagram_control.language = "language"
        return diagram_control

    def create_block(self, diagram_control=None):
        if diagram_control is None:
            diagram_control = self.create_diagram_control()

        System()
        block_model = BlockModel()
        System.add_port(self.create_port())

        block_model.ports = [{
                "type":"Test",
                "label":"Click",
                "conn_type":"Input",
                "name":"0"
                },{
                "type":"Test",
                "label":"Click",
                "conn_type":"Output",
                "name":"1"
                },{
                "type":"Test",
                "label":"Click",
                "conn_type":"Input",
                "name":"2"
                },{
                "type":"Test",
                "label":"Click",
                "conn_type":"Output",
                "name":"3"
                }
                ]


        block_model.help = "Test"
        block_model.label = "Test"
        block_model.color = "200:200:25:150"
        block_model.group = "Test"
        block_model.codes = {"code0":"Test",
                       "Code1":"Test",
                       "Code2":"Test"}
        block_model.type = "Test"
        block_model.language = "Test"
        block_model.properties = [{"name": "test",
                             "label": "Test",
                             "value": "0",
                             "type": MOSAICODE_FLOAT
                             }]
        block_model.extension = "Test"
        block_model.file = None

        result = BlockControl.load_ports(block_model, System.get_ports())
        System.add_block(block_model)
        self.assertEquals(result[1], "Success")
        self.assertEquals(result[0], True)
        self.assertEquals(len(block_model.ports),4)

        block = Block(diagram_control.diagram, block_model)
        self.assertEquals(len(block.ports),4)

        return block

    def create_comment(self, diagram = None):
        if diagram is None:
            comment = Comment(self.create_diagram(), None)
        else:
            comment = Comment(diagram, None)
        return comment

    def create_port(self):
        port = Port()
        port.type = "Test"
        port.language = "Test"
        port.hint = "Test"
        port.color = "#000"
        port.multiple = False
        port.file = None
        port.code = ""
        port.var_name = "$block[label]$_$block[id]$_$port[name]$"
        return port

    def create_code_template(self):
        code_template = CodeTemplate()
        code_template.name = "webaudio"
        code_template.type = "Test"
        code_template.language = "Test"
        code_template.command = "python\n"
        code_template.description = "Javascript / webaudio code template"

        code_template.code_parts = ["onload", "function", "declaration", "execution", "html"]
        code_template.properties = [{"name": "title",
                            "label": "Title",
                            "value": "Title",
                            "type": MOSAICODE_STRING
                            }
                           ]

        code_template.files["index.html"] = r"""
<html>
    <head>
        <meta http-equiv="Cache-Control" content="no-store" />
        <!-- $author$ $license$ -->
        <title>$prop[title]$</title>
        <link rel="stylesheet" type="text/css" href="theme.css">
        <script src="functions.js"></script>
        <script>
        $single_code[function]$
        function loadme(){
        $single_code[onload]$
        return;
        }
        var context = new (window.AudioContext || window.webkitAudioContext)();
        //declaration block
        $code[declaration]$

        //execution
        $code[execution]$

        //connections
        $connections$
        </script>
    </head>

    <body onload='loadme();'>
        $code[html]$
    </body>
</html>
"""

        code_template.files["theme.css"] = r"""
/*
Developed by: $author$
*/
html, body {
  background: #ffeead;
  color: #ff6f69;
}
h1, p {
  color: #ff6f69;
}
#navbar a {
  color: #ff6f69;
}
.item {
  background: #ffcc5c;
}
button {
  background: #ff6f69;
  color: #ffcc5c;
}
"""

        code_template.files["functions.js"] = r"""
/*
Developed by: $author$
*/
$single_code[function]$
"""
        System.add_code_template(code_template)
        return code_template
