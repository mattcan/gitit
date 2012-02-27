
class Gitit:
    """Controls interaction with git"""
    


    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin
        
    def _insert_controls(self):
        # Get the Gtk.UIManager
        manager = self._window.get_ui_manager()

        # Create a new action group
        self._action_group = Gtk.ActionGroup("GititPluginActions")
        self._action_group.add_actions([("GitCommit", None, _("Commit"),
                                         None, _("Opens the Git GUI to perform commit."),
                                         self._git_commit)])

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(ui_str)

    def _remove_controls(self):
        # Get the Gtk.UIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()
        
    def _tab_activation(self):
        print 'TAB ACTIVATED'
        
    def _git_commit(self):
        pass
