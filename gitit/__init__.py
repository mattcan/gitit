from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit
from gitit import Gitit

def DEBUG(message):
    """Prints a message to console when debugging is on"""
    
    debug_on = True
    if debug_on:
        print message

class GititPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GititPlugin"

    window = GObject.property(type=Gedit.Window)
    toolbar_ui_str = """<ui>
        <toolbar name="ToolBar">
            <separator/>
            <toolitem name="GitCommit" action="GitCommit"/>
        </toolbar>
    </ui>
    """

    def __init__(self, plugin, window):
        GObject.Object.__init__(self)
        #self.g = Gitit(plugin, window)
        
    def do_activate(self):
        DEBUG('Activating plugin...')
        
        #Attach signals
        self.window.set_data('GititPluginHandlers', self._signal_attach())
        
        # Insert menu items
        self._insert_controls()

    def do_update_state(self):
        # updates handled by signals
        pass

    def do_deactivate(self):
        DEBUG("Deactivating plugin...")
        
        handlers = self.window.get_data('GititPluginHandlers')
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            DEBUG("Disconnected handler " + str(handler_id))
            
        # Remove any installed menu items
        self._remove_controls()

        self._action_group = None
        
    def _insert_controls(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("GititPluginActions")
        self._action_group.add_actions([("GitCommit", "gtk-apply", "Commit",
                                         None, _("Opens the Git GUI to perform commit."),
                                         self._git_commit)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(self.toolbar_ui_str)

    def _remove_controls(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()
        
    def on_tab_activation(self, window, tab, data=None):
        #get name and path of currently active tab
        DEBUG('Fuck yea! A new tab is active, baby!')
        
        doc =  tab.get_document()
        uri = doc.get_uri_for_display()
        DEBUG('We are working with: ' + uri )
        
    def _signal_attach(self):
        handlers = []
        
        handler_id = self.window.connect('active-tab-changed', self.on_tab_activation)
        handlers.append(handler_id)
        DEBUG('Connected handler ' + str(handler_id))
        
        return handlers
        
    def _git_commit(self):
        pass
