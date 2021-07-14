import os
import json
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
gi.require_version('GtkSource', '4')
from gi.repository import GtkSource
from gi.repository import Pango

class SourceView:

    language_id = 'python'
    style_scheme_id = 'oblivion'
    
    def __init__(self):
        super().__init__()
        self._view = GtkSource.View()
        self._view.modify_font(Pango.FontDescription('monospace'))
        self._view.set_auto_indent(True)
        self._view.set_smart_home_end(True)
        self._view.set_highlight_current_line(True)
        self._view.set_tab_width(4)
        self._view.set_show_line_numbers(True)
        self._view.set_wrap_mode(Gtk.WrapMode.NONE)
        self._view.set_background_pattern(GtkSource.BackgroundPatternType.GRID)        
        self._buf = self._view.get_buffer()
        self._buf.set_highlight_syntax(True)      
        lang_manager = GtkSource.LanguageManager()
        lang = lang_manager.get_language(self.language_id)
        if None != lang :
            self._buf.set_language(lang)
        style_manager = GtkSource.StyleSchemeManager().get_default()
        style = style_manager.get_scheme(self.style_scheme_id)
        if None != style:
            self._buf.set_style_scheme(style)
        self._request_context = None
    
    
    @property
    def request_context(self):
        return self._request_context
        
        
    @request_context.setter
    def request_context(self, ctx):
        self._buf = self._view.get_buffer()
        if None == ctx:
            self._buf.set_text(None)
            return
        self._request_context = ctx
        self._buf.set_text(ctx.pretty_text)
        for event in ctx.events:
            self.append(event.get_source_text())
            self._file_path = ctx.file_path
        self._request_context = ctx
    
        
    @property
    def view(self):
        return self._view

    
    @view.setter
    def view(self, value):
        self._view = value


    @property
    def text(self):
        self._buf = self._view.get_buffer()
        startIter, endIter = self._buf.get_bounds()    
        text = self._buf.get_text(startIter, endIter, False) 
        return text
        
        
    def append(self, text):
        self._buf = self._view.get_buffer()
        end_iter = self._buf.get_end_iter()
        self._buf.insert(end_iter, "\n" + text)



