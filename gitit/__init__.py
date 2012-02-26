from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit
from gitit import Gitit

class GititPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GititPlugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self, plugin, window):
        GObject.Object.__init__(self)
        self.g = Gitit(plugin, window)
        
    def do_activate(self):
        # Insert menu items
        self.g.insert_controls()

    def do_update_state(self):
        # if update is a tab activation, call _gitit_manager
        self.g.tab_activation()

    def do_deactivate(self):
        # Remove any installed menu items
        self.g.remove_controls()

        self._action_group = None
