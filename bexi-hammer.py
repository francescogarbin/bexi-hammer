#! /usr/bin/python3

import sys
import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from classes.application import Application

if '__main__' == __name__:
    app = Application()
    app.run(sys.argv)

