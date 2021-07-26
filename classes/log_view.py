import os
import sys
from datetime import datetime
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Pango

class LogView:

    def __init__(self, text_view):
        self._view = text_view
        self._view.set_monospace(True)
        self._buf = self._view.get_buffer()
        self.tag_bold = self._buf.create_tag("bold", weight=Pango.Weight.BOLD)


    def clear(self):
        self._buf.set_text("")
    

    def append_request_context_events(self, events, clear_before=True):
        if clear_before:
            self.clear()
        if None == events:
            return
        for event in events:
            self.append_request_context_event(event)
 
    
    def append_request_context_event(self, event):
        if None == event:
            return
        if event.timestamp:
            time_format = "%d/%m/%y %H:%M:%S.%f"
            dt = datetime.utcfromtimestamp(event.timestamp)
            timestamp = "{}\n".format(dt.strftime(time_format))
            self._append_text(timestamp, True)
        if event.title:
            self._append_text("{}\n".format(event.title))
        if event.description:
            self._append_text("{}\n".format(event.description))
        if event.trace:
            self._append_text("{}\n".format(event.trace))
        self._append_text("\n")
    
    
    def _append_text(self, text, bold=False):
        start = self._buf.get_end_iter()
        if bold:
            self._buf.insert_markup(start, "<b>{}</b>".format(text), -1)
        else:
            self._buf.insert(start, text)

