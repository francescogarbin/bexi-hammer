import os
import sys
import json
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject
from .helpers import Helpers
from .log import Log as log


@Gtk.Template(filename="resources/settings_dialog.ui")
class SettingsDialog(Gtk.Dialog):

    __gtype_name__ = "settings_dialog"
    
    def __init__(self):
        super().__init__()

        
