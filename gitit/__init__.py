from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit
from gitit import GititHelper
from subprocess import call
import gitit_debug as _gd
import os

class GititPlugin(GObject.Object, Gedit.WindowActivatable):

    __gtype_name__ = "GititPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self, plugin, window):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        """Implement Gedit do_activate function"""
        _gd.DEBUG('Activating plugin...')
        
        self._gh = GititHelper(self, self.window)
        
        # Attach signals
        self._gh.attach_signals()
        # Insert menu items
        self._gh.insert_controls()

    def do_update_state(self):
        """Updates are being done based on signals"""
        pass

    def do_deactivate(self):
        """Implement Gedit do_deactivate function"""
        _gd.DEBUG("Deactivating plugin...")
        
        # remove signals
        self._gh.detach_signals()
        # Remove any installed menu items
        self._gh.remove_controls()
