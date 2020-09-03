import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from tests.mosaicode_tests. test_base import TestBase
from mosaicode.system import System as System
from mosaicode.GUI.blockstreeview import BlocksTreeView


class TestBlocksTreeView(TestBase):

    def setUp(self):
        block1 = self.create_block()
        block1.group = "Group1"

        block2 = self.create_block()
        block2.group = "Group2"

        block3 = self.create_block()
        block3.group = "Group2"

        self.widget = BlocksTreeView(
                    self.create_main_window(),
                    "Test",
                    {
                     "Test1" : block1,
                     "Test2" : block2,
                     "Test3" : block3
                     })

    def test_get_selected_block(self):
        self.widget.blocks_tree_view.set_cursor(0)
        self.widget.get_selected_block()

    def test_search(self):
        self.widget.search("Test")
        self.widget.search("None")
        self.widget.search("")
    
#    def test_row_activated(self):
#        treeselection = self.widget.blocks_tree_view.get_selection()
#        treeselection.select_iter(self.widget.tree_store.get_iter_first())
#        model, iterac = treeselection.get_selected()
#        path = model.get_path(iterac)
#        column = self.widget.blocks_tree_view.get_column(0)
#        self.blockstreeview.blocks_tree_view.row_activate(path, column)

    def test_events(self):
#        self.widget.blocks_tree_view.emit("cursor-changed")
#        self.widget.blocks_tree_view.emit("drag-data-get", Gtk.SelectionData().copy(), 0, 0, None)
#        self.widget.blocks_tree_view.emit("row_activated")
#        self.refresh_gui()
        pass
