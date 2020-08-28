from tests.mosaicode_tests.test_base import TestBase
from mosaicode.utils.FileUtils import *
from mosaicode.GUI.comment import Comment
from mosaicode.control.diagramcontrol import DiagramControl


class TestDiagramControl(TestBase):

    def setUp(self):
        self.diagram = self.create_full_diagram()
        self.diagram_control = DiagramControl(self.diagram)


    def test_add_block(self):
        block = self.create_block()
        self.diagram_control.add_block(block)

        block.language = "None"
        self.diagram_control.add_block(block)

        self.diagram.language = None
        self.diagram_control.add_block(block)

    def test_add_comment(self):
        comment = Comment(self.create_diagram(), None)
        self.diagram_control.add_comment(comment)
        self.diagram_control.add_comment(None)

    def test_copy(self):
        self.diagram_control.copy()

    def test_cut(self):
        self.diagram_control.cut()

    def test_delete(self):
        self.diagram_control.delete()

    def test_paste(self):
        self.diagram_control.paste()

    def test_add_connection(self):
        self.diagram_control.add_connection(None)

    def test_collapse_all(self):
        self.diagram_control.collapse_all(None)

    def test_align(self):
        for key in self.diagram.blocks:
            self.diagram.blocks[key].is_selected = True
        self.diagram_control.add_block(self.create_block())
        self.diagram_control.align("BOTTOM")
        self.diagram_control.align("TOP")
        self.diagram_control.align("LEFT")
        self.diagram_control.align("RIGHT")

    def test_do(self):
        self.diagram_control.do("Test")

    def test_set_show_grid(self):
        self.diagram_control.set_show_grid(None)
        self.diagram_control.set_show_grid(True)

    def test_undo_redo(self):
        self.diagram_control.redo()

        self.diagram_control.undo()
        self.diagram_control.redo()

        self.diagram = self.create_full_diagram()
        self.diagram_control.undo()

    def test_get_min_max(self):
        self.diagram_control.get_min_max()

    def test_load(self):
        self.diagram.file_name = None
        result = self.diagram_control.load()
        self.assertFalse(result, "Failed to load diagram")

        file_name = get_temp_file() + ".mscd"
        self.diagram_control.save(file_name)
        result = self.diagram_control.load(file_name)
        os.remove(file_name)
        self.assertTrue(result, "Failed to load diagram")

        diagram_control_load = self.create_diagram_control()
        result = diagram_control_load.load()

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


    def test_export_png(self):
        result = self.diagram_control.export_png(file_name=None)

        self.diagram.main_window.show_all()
        file_name = get_temp_file() + ".png"
        result = self.diagram_control.export_png(file_name)

