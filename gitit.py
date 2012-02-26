from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit

toolbar_ui_str = """<ui>
<toolbar name="ToolBar">
<separator/>
<toolitem name="GitCommit" action="GitCommit"/>
<toolitem name="GitPush" action="GitPush"/>
</toolbar>
</ui>
"""

class GititPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GititPlugin"

    window = GObject.property(type=Gedit.Window)

    def __init__(self, plugin, window):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        # Insert menu items
        self._insert_controls()

    def do_update_state(self):
        # if update is a tab activation, call _gitit_manager
        pass

    def do_deactivate(self):
        # Remove any installed menu items
        self._remove_controls()

        self._action_group = None

    def _insert_controls(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("GititPluginActions")
        self._action_group.add_actions([("GitCommit", None, _("Commit"),
                                         None, _("Opens the Git GUI to perform commit."),
                                         self._git_commit)],
                                       [("GitPush", None, _("Push"),
                                         None, _("Pushy pushy"), self._git_push)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_controls(self):
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()
