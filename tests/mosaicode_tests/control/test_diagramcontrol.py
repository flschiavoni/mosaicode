import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.model.connectionmodel import ConnectionModel
from mosaicode.system import System


class TestDiagramControl(TestBase):

    def setUp(self):
        self.diagram = self.create_full_diagram()
        self.diagram_control = DiagramControl(self.diagram)


    def test_add_block(self):
        block = self.create_block()
        diagram_control = DiagramControl(None)
        diagram_control.add_block(block)

        self.diagram_control.add_block(None)

        block = self.create_block()
        self.diagram_control.add_block(block)

        block.language = "None"
        self.diagram_control.add_block(block)

        self.diagram.language = None
        self.diagram_control.add_block(block)

    def test_select_all(self):
        self.diagram_control.select_all()
        diagram_control = DiagramControl(None)
        diagram_control.select_all()

    def test_cut(self):
        self.diagram_control.cut()
        diagram_control = DiagramControl(None)
        diagram_control.cut()

    def test_copy_delete_paste(self):
        for key in self.diagram.blocks:
            self.diagram.blocks[key].is_selected = True

        for key in self.diagram.blocks:
            self.diagram.blocks[key].language = "None"
            break

        for con in self.diagram.connectors: 
            con.is_selected = True
            break

        for comment in self.diagram.comments: 
            comment.is_selected = True
            break

        self.diagram_control.copy()
        self.diagram_control.delete()
        self.diagram_control.paste()

        diagram_control = DiagramControl(None)
        diagram_control.copy()
        diagram_control.delete()
        diagram_control.paste()


    def test_add_comment(self):
        comment = Comment(self.create_diagram(), None)
        self.diagram_control.add_comment(comment)
        self.diagram_control.add_comment(None)

    def test_add_connection(self):
        self.diagram_control.add_connection(None)
        connection = ConnectionModel(None, None, None, None, None)
        result = self.diagram_control.add_connection(connection)

    def test_collapse_all(self):
        self.diagram_control.collapse_all(None)

        diagram_control = DiagramControl(None)
        diagram_control.collapse_all(None)

    def test_align(self):
        for key in self.diagram.blocks:
            self.diagram.blocks[key].is_selected = True
        self.diagram_control.add_block(self.create_block())
        self.diagram_control.align("BOTTOM")
        self.diagram_control.align("TOP")
        self.diagram_control.align("LEFT")
        self.diagram_control.align("RIGHT")

        diagram_control = DiagramControl(None)
        diagram_control.align("RIGHT")

    def test_change_zoom(self):
        self.diagram_control.change_zoom(System.ZOOM_ORIGINAL)
        self.diagram_control.change_zoom(System.ZOOM_IN)
        self.diagram_control.change_zoom(System.ZOOM_OUT)

        diagram_control = DiagramControl(None)
        diagram_control.change_zoom(System.ZOOM_ORIGINAL)

    def test_do(self):
        self.diagram_control.do("Test")

        diagram_control = DiagramControl(None)
        diagram_control.do("Test")

    def test_set_show_grid(self):
        self.diagram_control.set_show_grid(None)
        self.diagram_control.set_show_grid(True)


    def test_undo_redo(self):
        self.diagram_control.redo()

        self.diagram_control.undo()
        self.diagram_control.redo()

        diagram_control = DiagramControl(None)
        diagram_control.undo()
        diagram_control.redo()

        while len(self.diagram.undo_stack) > 1: 
            self.diagram.undo_stack.pop() 
        self.diagram_control.undo()
        self.diagram_control.undo()

    def test_load(self):
        self.diagram.file_name = None
        result = self.diagram_control.load()
        self.assertFalse(result[0], None)

        file_name = get_temp_file() + ".mscd"
        self.diagram_control.save(file_name)
        result = self.diagram_control.load(file_name)
        os.remove(file_name)

        diagram_control_load = self.create_diagram_control()
        result = diagram_control_load.load()

        diagram_control = DiagramControl(None)
        diagram_control.load(None)


    def test_save(self):
        file_name = get_temp_file() + ".mscd"
        result = self.diagram_control.save(file_name)
        os.remove(file_name)
        self.assertTrue(result, "Failed to save diagram")

        file_name = get_temp_file()
        result = self.diagram_control.save(file_name)
        os.remove(file_name + ".mscd")
        self.assertTrue(result, "Failed to save diagram")

        self.diagram.file_name = None
        result = self.diagram_control.save()
        os.remove(self.diagram.file_name)
        self.assertTrue(result, "Failed to save diagram")
