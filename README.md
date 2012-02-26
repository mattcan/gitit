# Gitit

## A git plugin for gEdit

---

Gitit is a plugin for gEdit that works similarily to msysgit with Visual Studio.
Instead of creating the functionality of git-gui and gitk in gEdit, Gitit simply
calls those tools. They do a good job working with git and this plugin makes the
functionality more accessible than running those tools from the [External Tools][ExtTools]
plugin.

### Requirements

You will need to download the following software for Gitit to run.

 * gitk
 * git-gui
 
In Ubuntu, simply run the following command in a terminal:

    sudo apt-get install gitk git-gui
    
### Features

Gitit is still under development and is lacking most of the features required for
a proper git plugin to function. 

 * Commit
    
    Commit runs git-gui which has the power to do your *add*s at the same time
    as you put together your commit message. There is also a window that loads
    the diff for each file listed.
    
[ExtTools]: http://live.gnome.org/Gedit/Plugins/ExternalTools
