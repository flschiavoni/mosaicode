# -*- coding: utf-8 -*-
"""
This module contains the MainControl class.
"""
import gettext
import os
import signal
import subprocess
from copy import deepcopy
from threading import Thread

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from mosaicode.control.blockcontrol import BlockControl
from mosaicode.control.codegenerator import CodeGenerator
from mosaicode.control.codetemplatecontrol import CodeTemplateControl
from mosaicode.control.diagramcontrol import DiagramControl
from mosaicode.control.portcontrol import PortControl
from mosaicode.control.publisher import Publisher
from mosaicode.GUI.about import About
from mosaicode.GUI.codewindow import CodeWindow
from mosaicode.GUI.diagram import Diagram
from mosaicode.GUI.messagedialog import MessageDialog
from mosaicode.GUI.confirmdialog import ConfirmDialog
from mosaicode.GUI.savedialog import SaveDialog
from mosaicode.GUI.opendialog import OpenDialog
from mosaicode.GUI.preferencewindow import PreferenceWindow
from mosaicode.GUI.selectcodetemplate import SelectCodeTemplate
from mosaicode.persistence.preferencespersistence import PreferencesPersistence
from mosaicode.system import System as System

_ = gettext.gettext


class MainControl():
    """
    This class contains methods related the MainControl class.
    """
    # ----------------------------------------------------------------------

    def __init__(self, main_window):
        self.main_window = main_window
        self.open_dialog = None
        self.save_dialog = None
        self.confirm_dialog = None
        self.preference_window = None
        self.message_dialog = None
        self.about_window = None
        self.code_window = None

        # Clipboard is here because It must be possible to exchange data between diagrams
        self.clipboard = []
        self.threads = {}
        self.publisher = Publisher()

    # ----------------------------------------------------------------------
    def init(self):
        self.update_blocks()
        # Load plugins
        for plugin in System.get_plugins():
            plugin.load(self.main_window)

        self.main_window.menu.update_recent_files()
        self.main_window.menu.update_examples()

    # ----------------------------------------------------------------------
    def get_current_diagram(self):
        return self.main_window.work_area.get_current_diagram()

    # ----------------------------------------------------------------------
    def update_blocks(self):
        System.reload()
        self.main_window.menu.update_blocks()
        self.main_window.block_notebook.update_blocks()

    # ----------------------------------------------------------------------
    def new(self):
        """
        This method create a new the diagram file.
        """
        Diagram(self.main_window)

    # ----------------------------------------------------------------------
    def select_open(self, path=None):
        """
        This method open a selected file.
        """
        if path is None:
            path = System.get_user_dir()
        self.open_dialog = OpenDialog(
            "Open Diagram",
            self.main_window,
            filetype="mscd",
            path=path
            )
        file_name = self.open_dialog.run()
        if file_name is None or file_name == "":
            return
        self.open(file_name)

    # ----------------------------------------------------------------------
    def open(self, file_name):
        """
        This method open a file.
        """
        diagram = Diagram(self.main_window)
        result = DiagramControl(diagram).load(file_name)
        if result[0] is None:
            self.message_dialog = MessageDialog("Error", result[1], self.main_window)
            self.message_dialog.run()
            return
        diagram = result[0]
        System.add_recent_files(file_name)

    # ----------------------------------------------------------------------
    def close(self):
        """
        This method closes a tab on the work area.
        """
        self.main_window.work_area.close_tab()

    # ----------------------------------------------------------------------
    def __select_save(self, diagram):
        """
        This method selects a name to save the file.
        """
        while True:
            file_name = diagram.file_name
            if file_name == "Untitled":
                file_name = System.get_user_dir() + "/" + diagram.file_name
            self.save_dialog = SaveDialog(
                self.main_window,
                title=_("Save Diagram"),
                filename=file_name,
                filetype="*.mscd")
            name = self.save_dialog.run()
            if name is None:
                return False, "User canceled the operation"

            if os.path.exists(name) is True:
                msg = _("File exists. Overwrite?")
                self.confirm_dialog = ConfirmDialog(msg, self.main_window)
                result = self.confirm_dialog.run()
                if result == Gtk.ResponseType.CANCEL:
                    continue
            if not name.endswith("mscd"):
                name = name + ".mscd"
            diagram.file_name = name
            break
        return True, "Success"

    # ----------------------------------------------------------------------
    def save(self, save_as=False):
        """
        This method save the file.
        """
        diagram = self.get_current_diagram()
        if diagram is None:
            return False

        if diagram.file_name is "Untitled" or save_as:
            result, message = self.__select_save(diagram)
            if not result:
                return False

        result, message = DiagramControl(diagram).save()
        if not result:
            self.message_dialog = MessageDialog("Error", message, self.main_window)
            self.message_dialog.run()
            return False
        System.add_recent_files(diagram.file_name)
        self.main_window.work_area.rename_diagram(diagram)
        return True

    # ----------------------------------------------------------------------
    def save_as(self):
        """
        This method save as.
        """
        self.save(save_as=True)

    # ----------------------------------------------------------------------
    def exit(self, widget=None, data=None):
        """
        This method close main window.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        PreferencesPersistence.save(
                System.get_preferences(),
                System.get_user_dir()
                )
        if self.main_window.work_area.close_tabs():
            Gtk.main_quit()
        else:
            return True
    # ----------------------------------------------------------------------
    def add_recent_files(self, file_name):
        System.add_recent_files(file_name)
        self.main_window.menu.update_recent_files()
        PreferencesPersistence.save(
            System.get_preferences(),
            System.get_user_dir()
            )

    # ----------------------------------------------------------------------

    def get_clipboard(self):
        """
        This method return the clipboard.
        """
        return self.clipboard

    # ----------------------------------------------------------------------
    def reset_clipboard(self):
        """
        This method clear the clipboard.
        """
        self.clipboard = []

    # ----------------------------------------------------------------------
    def preferences(self):
        """
        """
        self.preference_window = PreferenceWindow(self.main_window)
        self.preference_window.run()

    # ----------------------------------------------------------------------
    def save_source(self, codes=None, generator=None):
        """
        This method saves the source codes.
        """
        diagram = self.get_current_diagram()
        result, msg = CodeGenerator.save_source(
            diagram=diagram,
            codes=codes,
            generator=generator
            )
        if not result:
            self.message_dialog = MessageDialog("Error", msg, self.main_window)
            self.message_dialog.run()

    # ----------------------------------------------------------------------
    def view_source(self):
        """
        This method view the source code.
        """
        diagram = self.get_current_diagram()
        generator, msg = CodeGenerator.get_code_generator(diagram)
        if generator is not None:
            codes = generator.generate_code()
            self.code_window = CodeWindow(self.main_window, codes)
            self.code_window.run()
            self.code_window.close()
            self.code_window.destroy()
        else:
            self.message_dialog = MessageDialog("Error", msg, self.main_window)
            self.message_dialog.run()

    # ----------------------------------------------------------------------
    def run(self, codes=None):
        """
        This method runs the code.
        """
        diagram = self.get_current_diagram()
        generator, message = CodeGenerator.get_code_generator(diagram)
        if generator is None:
            return False

        self.save_source(codes=codes, generator=generator)

        command = diagram.code_template.command
        command = command.replace("$dir_name$", System.get_dir_name(diagram))

        def __run(self):
            process = subprocess.Popen(
                command,
                cwd=System.get_dir_name(diagram),
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid
                )
            self.threads[thread] = diagram, process
            self.main_window.toolbar.update_threads(self.threads)
            (stdout_data, stderr_data) = process.communicate()
            System.log(stdout_data + "\n")
            System.log(stderr_data + "\n")
            del self.threads[thread]
            self.main_window.toolbar.update_threads(self.threads)

        System.log("Executing Code:\n" + command)
        thread = Thread(target=__run, args=(self,))
        thread.start()

        return True

    # ----------------------------------------------------------------------
    def stop(self, widget, process):
        if process is None:
            return
        pgid = os.getpgid(process.pid)
        os.killpg(pgid, signal.SIGTERM)

    # ----------------------------------------------------------------------
    def publish(self):
        """
        This method run web server.
        """
        if self.publisher.is_running():
            self.publisher.stop()
        else:
            self.publisher.start()

    # ----------------------------------------------------------------------
    def about(self):
        """
        This method open the about window.
        """
        self.about_window = About(self.main_window)
        self.about_window.show_all()

    # ----------------------------------------------------------------------
    def search(self, query):
        """
        This method search the query in the blocks_tree_view.
        """
        self.main_window.block_notebook.search(query)

    # ----------------------------------------------------------------------
    def set_block(self, block):
        """
        This method set the block properties.
        """
        self.main_window.property_box.set_block(block)

    # ----------------------------------------------------------------------
    def get_selected_block(self):
        """
        This method get the tree view block.
        """
        return self.main_window.block_notebook.get_selected_block()

    # ----------------------------------------------------------------------
    def clear_console(self):
        """
        This method clear the console.
        """
        self.main_window.status.clear()

    # ----------------------------------------------------------------------
    def add_block(self, block):
        """
        This method add a block.

        Parameters:

                * **Types** (:class:`block<>`)
        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        result = DiagramControl(self.get_current_diagram()).add_block(block)
        if not result[0]:
            message = result[1]
            self.message_dialog = MessageDialog("Error", message, self.main_window )
            self.message_dialog.run()
            return None
        return block

    # ----------------------------------------------------------------------
    def add_comment(self, comment=None):
        """
        This method add a block.

        Parameters:

                * **Types** (:class:`block<>`)
        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        DiagramControl(self.get_current_diagram()).add_comment(comment)
        return True

    # ----------------------------------------------------------------------
    def select_all(self):
        DiagramControl(self.get_current_diagram()).select_all()

    # ----------------------------------------------------------------------
    def cut(self):
        """
        This method cut a block on work area.
        """
        DiagramControl(self.get_current_diagram()).cut()

    # ----------------------------------------------------------------------
    def copy(self):
        """
        This method copy a block.
        """
        DiagramControl(self.get_current_diagram()).copy()

    # ----------------------------------------------------------------------
    def paste(self):
        """
        This method paste a block.
        """
        DiagramControl(self.get_current_diagram()).paste()

    # ----------------------------------------------------------------------
    def delete(self):
        """
        This method delete a block.
        """
        DiagramControl(self.get_current_diagram()).delete()

    # ----------------------------------------------------------------------
    def zoom_in(self):
        """
        This method increases the zoom value.
        """
        DiagramControl(self.get_current_diagram()).change_zoom(System.ZOOM_IN)

    # ----------------------------------------------------------------------
    def zoom_out(self):
        """
        This method decreases the zoom.
        """
        DiagramControl(self.get_current_diagram()).change_zoom(System.ZOOM_OUT)

    # ----------------------------------------------------------------------
    def zoom_normal(self):
        """
        Set the zoom value to normal.
        """
        DiagramControl(self.get_current_diagram()).change_zoom(System.ZOOM_ORIGINAL)

    # ----------------------------------------------------------------------
    def undo(self):
        """
        Undo a modification.
        """
        DiagramControl(self.get_current_diagram()).undo()

    # ----------------------------------------------------------------------
    def redo(self):
        """
        Redo a modification.
        """
        DiagramControl(self.get_current_diagram()).redo()

    # ----------------------------------------------------------------------
    def align_top(self):
        DiagramControl(self.get_current_diagram()).align("TOP")

    # ----------------------------------------------------------------------
    def align_bottom(self):
        DiagramControl(self.get_current_diagram()).align("BOTTOM")

    # ----------------------------------------------------------------------
    def align_left(self):
        DiagramControl(self.get_current_diagram()).align("LEFT")

    # ----------------------------------------------------------------------
    def align_right(self):
        DiagramControl(self.get_current_diagram()).align("RIGHT")

    # ----------------------------------------------------------------------
    def collapse_all(self):
        DiagramControl(self.get_current_diagram()).collapse_all(True)

    # ----------------------------------------------------------------------
    def uncollapse_all(self):
        DiagramControl(self.get_current_diagram()).collapse_all(False)

    # ----------------------------------------------------------------------
    def redraw(self, show_grid):
        diagrams = self.main_window.work_area.get_diagrams()
        for diagram in diagrams:
            DiagramControl(diagram).set_show_grid(show_grid)

    # ----------------------------------------------------------------------
    def show_grid(self, event):
        if event is None:
            return
        self.redraw(event.get_active())
    # ----------------------------------------------------------------------
    def add_code_template(self, code_template):
        CodeTemplateControl.add_code_template(code_template)
        System.reload()

    # ----------------------------------------------------------------------
    def delete_code_template(self, code_template_name):
        result = CodeTemplateControl.delete_code_template(code_template_name)
        if not result[0]:
            self.message_dialog = MessageDialog("Error", result[1], self.main_window)
            self.message_dialog.run()
            return False
        self.message_dialog = MessageDialog("Info", result[1], self.main_window)
        self.message_dialog.run()
        System.reload()
        return True

    # ----------------------------------------------------------------------
    def add_port(self, port):
        PortControl.add_port(port)
        System.reload()

    # ----------------------------------------------------------------------
    def delete_port(self, port_key):
        result = PortControl.delete_port(port_key)
        if not result[0]:
            self.message_dialog = MessageDialog("Error", result[1], self.main_window)
            self.message_dialog.run()
        System.reload()

    # ----------------------------------------------------------------------
    def add_new_block(self, block):
        BlockControl.add_new_block(block)
        self.update_blocks()

    # ----------------------------------------------------------------------
    def delete_block(self, block):
        result = BlockControl.delete_block(block)
        if not result[0]:
            self.message_dialog = MessageDialog("Error", result[1], self.main_window)
            self.message_dialog.run()
        self.update_blocks()

    # ----------------------------------------------------------------------
    def update_all(self):
        for diagram in self.main_window.work_area.get_diagrams():
            diagram.update()

# ----------------------------------------------------------------------
