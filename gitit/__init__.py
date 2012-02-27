from gettext import gettext as _
from gi.repository import GObject, Gtk, Gedit
from gitit import Gitit
from subprocess import call
import os

def DEBUG(message):
    """Prints a message to console when debugging is on"""
    
    debug_on = True
    if debug_on:
        print message

class GititPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "GititPlugin"
    
    SIG_HANDLER = 'GititPluginHandler'

    window = GObject.property(type=Gedit.Window)
    toolbar_ui_open = """<ui>
        <toolbar name="ToolBar">
            <separator/>"""
    toolbar_ui_close = """
        </toolbar>
    </ui>
    """

    def __init__(self, plugin, window):
        GObject.Object.__init__(self)
        
    def do_activate(self):
        """Implement Gedit do_activate function"""
        DEBUG('Activating plugin...')
        
        # Attach signals
        self._attach_signals()
        # Insert menu items
        self._insert_controls()

    def do_update_state(self):
        """Implement Gedit do_update_state function"""
        pass

    def do_deactivate(self):
        """Implement Gedit do_deactivate function"""
        DEBUG("Deactivating plugin...")
        
        # remove signals
        self._remove_signals()
        # Remove any installed menu items
        self._remove_controls()
        self._action_group = None
        
    def _insert_controls(self, in_repo=True):
        """Insert the controls defined in self.toolbar_ui_string into the toolbar"""
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Create ActionGroup for repo control items
        self._action_group = Gtk.ActionGroup("GititPluginActions")
        if in_repo:
            self._action_group.add_actions([("GitCommit", Gtk.STOCK_APPLY, _("Commit"),
                                         None, _("Opens the Git GUI to perform commit."),
                                         self._git_commit)])
            toolbar_ui_items = """
            <toolitem name="GitCommit" action="GitCommit"/>"""
        else:
            self._action_group.add_actions([("GitInit", Gtk.STOCK_DND, _("Initialize"),
                                         None, _("Initialize a new repository."),
                                         self._git_init)])
            toolbar_ui_items = """
            <toolitem name="GitInit" action="GitInit"/>"""

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)
        
        toolbar_ui_str = self.toolbar_ui_open + toolbar_ui_items + self.toolbar_ui_close

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(toolbar_ui_str)

    def _remove_controls(self):
        """Remove the toolbar controls"""
        # Get the Gtk.UIManager
        manager = self.window.get_ui_manager()

        # Remove the ui
        manager.remove_ui(self._ui_id)

        # Remove the action group
        manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()
        
    def on_tab_activation(self, window, tab, data=None):
        """Get the URI of the active document, if the document is in a
           git repo than show certain tools and if not than show different
           tools"""
        DEBUG('New tab activated.')
        
        # get the document uri
        doc =  tab.get_document()
        uri = self._get_uri(doc)
        
        is_in_repo = self._check_in_repo(uri)
        
        if is_in_repo:
            # build menu with repo commands
            # show the repo and branch names in statusbar
            pass
        else:
            # build menu with init command only
            # clear status bar if we have it
            pass
        
    def _get_uri(self, document):
        """gets the uri of the document and formats it for use"""
    
        #get the uri of the document, which includes the filename
        uri_orig = document.get_uri_for_display()
        
        #remove the file name
        uri_parts = uri_orig.split('/')
        filename = uri_parts.pop(-1)
        
        # if the uri was just a file name (because its a new file) than
        # popping will cause an empty list
        if len(uri_parts) == 0: uri = ''
        else: uri = '/'.join(uri_parts)
        
        DEBUG('URI: ' + uri)
        DEBUG('File: ' + filename)
        
        return uri
        
    def _check_in_repo(self, uri):
        """check if we're working in a git repo"""
        
        #exit quick if there is an empty uri
        if uri == '': return False
        
        # create command line arguements
        change_path = 'cd %s' % uri
        git_check = 'git rev-parse --is-inside-git-dir'
        
        #run commands and get last called command return code to check against
        retcode = call(change_path + ';' + git_check, shell=True)
        
        if (retcode == 1) or (retcode == 0):    # retcode is true/false if in a repo
            DEBUG('In repo ' + str(retcode))
            return True
        else:                                   # retcode is 128 if outside of repo
            DEBUG('NOT in repo ' + str(retcode))
            return False
            
    def _attach_signals(self):
        """Attach all signals here"""
        
        handlers = []
        handler_id = self.window.connect('active-tab-changed', self.on_tab_activation)
        handlers.append(handler_id)
        DEBUG('Connected handler ' + str(handler_id))
        
        self.window.set_data(self.SIG_HANDLER, handlers)
        
    def _detach_signals(self):
        """Removes all the signals in use"""
        
        handlers = self.window.get_data(self.SIG_HANDLER)
        for handler_id in handlers:
            self.window.disconnect(handler_id)
            DEBUG('Disconnected handler ' + str(handler_id))
        
    def _git_commit(self):
        pass
