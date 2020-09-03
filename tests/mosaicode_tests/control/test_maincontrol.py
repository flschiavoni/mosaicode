import gi
import os
import unittest
import threading
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from time import sleep

from tests.mosaicode_tests.test_base import TestBase
from mosaicode.control.maincontrol import MainControl
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.model.plugin import Plugin
from mosaicode.system import System

class TestMainControl(TestBase):

    def setUp(self):
        self.main_window = self.create_main_window()
        self.main_control = MainControl(self.main_window)
        self.main_control.init()
        self.diagram = self.create_full_diagram(main_window=self.main_window)
        self.main_window.work_area.add_diagram(self.diagram)
        self.diagram.set_modified(False)

    def test_init(self):
        System()
        System.add_plugin(Plugin())
        self.main_control.init()

    def test_select_open(self):
        t1 = threading.Thread(target=self.main_control.select_open, args=(None,))
        t1.start()
        sleep(1)
        if self.main_control.open_dialog:
            self.main_control.open_dialog.response(Gtk.ResponseType.CANCEL)
        t1.join()

        diagram = self.create_full_diagram(main_window=self.main_window)
        diagram.file_name = "/tmp/Test.mscd"
        DiagramControl(diagram).save()
        path = "/tmp/"
        System.set_user_dir(path)

        t1 = threading.Thread(target=self.main_control.select_open, args=(path,))
        t1.start()
        sleep(1)
        if self.main_control.open_dialog:
            self.main_control.open_dialog.set_filename("/tmp/Test.mscd")
            self.main_control.open_dialog.response(Gtk.ResponseType.OK)
        t1.join()
        os.remove("/tmp/Test.mscd")

    def test_open(self):
        t1 = threading.Thread(target=self.main_control.open, args=("Test",))
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_save(self):
        # diagram is null
        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        t1 = threading.Thread(target=self.main_control.save, args=(None,))
        t1.start()
        sleep(1)
        if self.main_control.save_dialog:
            self.main_control.save_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

        self.main_control.new()
        t1 = threading.Thread(target=self.main_control.save, args=(None,))
        t1.start()
        sleep(1)
        if self.main_control.save_dialog:
            self.main_control.save_dialog.response(Gtk.ResponseType.OK)
        self.refresh_gui()
        t1.join()

        # Cancel button
        self.main_control.new()
        t1 = threading.Thread(target=self.main_control.save, args=(None,))
        t1.start()
        sleep(1)
        if self.main_control.save_dialog:
            self.main_control.save_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_save_as(self):
        t1 = threading.Thread(target=self.main_control.save_as, args=())
        t1.start()
        sleep(1)
        if self.main_control.save_dialog:
            self.main_control.save_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_exit(self):
        self.main_control.exit()

        self.main_window = self.create_main_window()
        self.main_control = MainControl(self.main_window)
        self.main_control.init()
        self.main_control.new()

        diagram = self.main_window.work_area.get_current_diagram()
        diagram.set_modified(True)

        t1 = threading.Thread(target=self.main_control.exit, args=())
        t1.start()
        sleep(1)
        if self.main_window.work_area.confirm:
            self.main_window.work_area.confirm.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_add_recent_files(self):
        self.main_control.add_recent_files("Test")
        self.main_control.add_recent_files("Test")
        for i in range(0,20):
            System.get_preferences().recent_files.append("Some File")
        self.main_control.add_recent_files("Test")
 
    def test_clipboard(self):
        self.main_control.get_clipboard()
        self.main_control.reset_clipboard()

    def test_preferences(self):
        t1 = threading.Thread(target=self.main_control.preferences, args=())
        t1.start()
        sleep(1)
        if self.main_control.preference_window:
            self.main_control.preference_window.close()
        self.refresh_gui()
        t1.join()

    def test_save_source(self):
        self.main_control.save_source()

        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        t1 = threading.Thread(target=self.main_control.save_source, args=())
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.close()
        t1.join()

    def test_view_source(self):
        t1 = threading.Thread(target=self.main_control.view_source, args=())
        t1.start()
        sleep(2)
        if self.main_control.code_window:
            self.main_control.code_window.close()
        self.refresh_gui()
        t1.join()

        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        t1 = threading.Thread(target=self.main_control.view_source, args=())
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_run_stop(self):
        self.main_control.run()
        sleep(1)
        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        self.main_control.run()
        self.main_control.stop(None, None)
        self.main_control.update_blocks()
        self.main_control.close()
        self.main_control.new()

    def test_publish(self):
        self.main_control.publish()
        # Twice to start / stop
        self.main_control.publish()

    def test_about(self):
        t1 = threading.Thread(target=self.main_control.about, args=())
        t1.start()
        sleep(1)
        if self.main_control.about_window:
            self.main_control.about_window.close()
        self.refresh_gui()
        t1.join()

    def test_search_clear(self):
        self.main_control.search("Test")
        self.main_control.set_block(self.create_block())
        self.main_control.get_selected_block()
        self.main_control.clear_console()
        self.main_control.show_grid(None)
        self.main_window.menu.show_grid.emit("activate")
        
    def test_add_block(self):
        self.main_control.add_block(self.create_block())

        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()

        t1 = threading.Thread(
            target=self.main_control.add_block,
            args=(self.create_block(),)
            )
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_edit(self):
        self.main_control.add_comment()
        self.main_control.select_all()
        self.main_control.cut()
        self.main_control.copy()
        self.main_control.paste()
        self.main_control.delete()

        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        self.main_control.add_comment()
        self.main_control.select_all()
        self.main_control.cut()
        self.main_control.copy()
        self.main_control.paste()
        self.main_control.delete()

    def test_properties(self):
        self.main_control.zoom_in()
        self.main_control.zoom_out()
        self.main_control.zoom_normal()
        self.main_control.align_bottom()
        self.main_control.align_top()
        self.main_control.align_left()
        self.main_control.align_right()
        self.main_control.collapse_all()
        self.main_control.uncollapse_all()

        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        self.main_control.zoom_in()
        self.main_control.zoom_out()
        self.main_control.zoom_normal()
        self.main_control.align_bottom()
        self.main_control.align_top()
        self.main_control.align_left()
        self.main_control.align_right()
        self.main_control.collapse_all()
        self.main_control.uncollapse_all()

    def test_undo_redo(self):
        self.main_control.undo()
        self.main_control.redo()

        self.diagram.set_modified(False)
        self.main_window.work_area.close_tabs()
        self.main_control.undo()
        self.main_control.redo()

    def test_redraw_update(self):
        self.main_control.redraw(True)
        self.main_control.redraw(False)
        self.main_control.update_all()

    def test_add_delete_code_template(self):
        self.main_control.add_code_template(self.create_code_template())

        t1 = threading.Thread(
            target=self.main_control.delete_code_template,
            args=(self.create_code_template(),)
            )
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

        code_template = self.create_code_template()
        System.add_code_template(code_template)
        t1 = threading.Thread(
            target=self.main_control.delete_code_template,
            args=(code_template,)
            )
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_add__delete_port(self):
        self.main_control.add_port(self.create_port())

        t1 = threading.Thread(target=self.main_control.delete_port, args=("port",))
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()

    def test_add_delete_block(self):
        self.main_control.add_new_block(self.create_block())

        t1 = threading.Thread(
            target=self.main_control.delete_block,
            args=(self.create_block(),)
            )
        t1.start()
        sleep(1)
        if self.main_control.message_dialog:
            self.main_control.message_dialog.response(Gtk.ResponseType.CANCEL)
        self.refresh_gui()
        t1.join()
