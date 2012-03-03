from gettext import gettext as _
from subprocess import call
from gi.repository import Gtk

#custom modules
import gitwrapper
import gitit_debug as _gd

class GititHelper:
    
    SIG_HANDLER = 'GititPluginHandler'
    toolbar_ui_open = """<ui>
        <toolbar name="ToolBar">
            <separator/>"""
    toolbar_ui_close = """
        </toolbar>
    </ui>
    """
    
    def __init__(self, plugin, window):
        self._plugin = plugin
        self._window = window
        self._git = gitwrapper.GitWrapper()
        
    def on_tab_activation(self, window, tab, data=None):
        """Get the URI of the active document, if the document is in a
           git repo than show certain tools and if not than show different
           tools"""
        _gd.DEBUG('New tab activated.')
        
        # get the document uri
        doc =  tab.get_document()
        uri = self._get_uri(doc)
        
        #brand new document so nowhere to init or commit
        #TODO change this to show an init and make the user save
        if uri == '':
            self.remove_controls()
            return
        
        is_in_repo = self._check_in_repo(uri)
        
        self._rebuild_controls(is_in_repo)
        #call a statusbar rebuild here
        
    def insert_controls(self, in_repo=True):
        """Insert the controls defined in self.toolbar_ui_string into the toolbar"""
        _gd.DEBUG('Inserting controls..')
        
        # Get the Gtk.UIManager
        manager = self._window.get_ui_manager()

        # Create ActionGroup for repo control items
        self._action_group = Gtk.ActionGroup("GititPluginActions")
        if in_repo:
            self._action_group.add_actions([("GitCommit", Gtk.STOCK_APPLY, _("Commit"),
                                         None, _("Opens the Git GUI to perform commit."),
                                         self._git.commit)])
            toolbar_ui_items = """
            <toolitem name="GitCommit" action="GitCommit"/>"""
        else:
            self._action_group.add_actions([("GitInit", Gtk.STOCK_DND, _("Initialize"),
                                         None, _("Initialize a new repository."),
                                         self._git.init)])
            toolbar_ui_items = """
            <toolitem name="GitInit" action="GitInit"/>"""

        # Insert the action group
        manager.insert_action_group(self._action_group, -1)
        
        toolbar_ui_str = self.toolbar_ui_open + toolbar_ui_items + self.toolbar_ui_close

        # Merge the UI
        self._ui_id = manager.add_ui_from_string(toolbar_ui_str)

    def remove_controls(self):
        """Remove the toolbar controls"""
        _gd.DEBUG('Removing controls...')
        
        # Get the Gtk.UIManager
        manager = self._window.get_ui_manager()

        # Remove the ui
        if self._ui_id: manager.remove_ui(self._ui_id)

        # Remove the action group
        if self._action_group: manager.remove_action_group(self._action_group)

        # Make sure the manager updates
        manager.ensure_update()
        
    def _rebuild_controls(self, in_repo):
        """Removes and re-adds the controls. Passes whether or not currently in
        a repo"""
        _gd.DEBUG('Rebuilding controls...')
        self.remove_controls()
        self.insert_controls(in_repo)
        
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
        
        _gd.DEBUG('URI: ' + uri)
        _gd.DEBUG('File: ' + filename)
        
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
            _gd.DEBUG('In repo ' + str(retcode))
            return True
        else:                                   # retcode is 128 if outside of repo
            _gd.DEBUG('NOT in repo ' + str(retcode))
            return False
            
    def attach_signals(self):
        """Attach all signals here"""
        
        handlers = []
        handler_id = self._window.connect('active-tab-changed', self.on_tab_activation)
        handlers.append(handler_id)
        _gd.DEBUG('Connected handler ' + str(handler_id))
        
        self._window.set_data(self.SIG_HANDLER, handlers)
        
    def detach_signals(self):
        """Removes all the signals in use"""
        
        handlers = self._window.get_data(self.SIG_HANDLER)
        for handler_id in handlers:
            self._window.disconnect(handler_id)
            _gd.DEBUG('Disconnected handler ' + str(handler_id))
