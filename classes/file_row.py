import os, sys, gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from .request_context import RequestContextStatus

class FileRow(Gtk.ListBoxRow):

    _ui_file = "resources/file_row_v1.ui"
    
    @staticmethod
    def create_from_request_context(ctx):
        builder = Gtk.Builder()
        builder.add_from_file(FileRow._ui_file)
        box = builder.get_object('file_row_box')
        row = FileRow()
        row.add(box)
        row._run_image = builder.get_object('run_image')
        row._type_label = builder.get_object('type_label')
        row._name_label = builder.get_object('name_label')
        row._status_image = builder.get_object('status_image')
        service_code = ctx.get_attribute('cod_servizio')
        flow_code = ctx.get_attribute('cod_flusso')
        row.file_type = "{} {}".format(service_code, flow_code)
        row.file_path = ctx.file_path
        row.file_name = ctx.file_name
        row._request_context_id = ctx.identifier
        row.set_status_image(ctx.status)
        return row


    def __init__(self):
        super(Gtk.ListBoxRow, self).__init__()
        self._request_context_id = None
        self._type_label = None
        self._name_label = None
        self._status_image = None
        self._file_path = None
        self._run_image = None
        self.connect("enter-notify-event", self.on_enter)


    def hide_status(self):
        self._status_image.hide()
    
    
    def set_status_image(self, request_context_status):
        icon_size = Gtk.IconSize.MENU
        if RequestContextStatus.Idle == request_context_status: 
            self._status_image.hide()
        elif RequestContextStatus.Running == request_context_status:
            self._status_image.set_from_pixbuf(self._run_image.get_pixbuf())        
            self._status_image.show()
        elif RequestContextStatus.Completed == request_context_status:
            self._status_image.set_from_stock(Gtk.STOCK_OK, icon_size)
            self._status_image.show()
        elif RequestContextStatus.Completed_WARN == request_context_status:
            self._status_image.set_from_stock(Gtk.STOCK_DIALOG_WARNING, icon_size)
            self._status_image.show()
        elif RequestContextStatus.Completed_NOT_OK == request_context_status:
            self._status_image.set_from_stock(Gtk.STOCK_DIALOG_WARNING, icon_size)
            self._status_image.show()
        elif RequestContextStatus.Error == request_context_status:
            self._status_image.set_from_stock(Gtk.STOCK_DIALOG_ERROR, icon_size)
            self._status_image.show()
        elif RequestContextStatus.Undefined == request_context_status:
            self._status_image.set_from_stock(Gtk.STOCK_DIALOG_QUESTION, icon_size)
            self._status_image.show()
        else:
            self._status_image.hide()
            raise Exception("Invalid request_context_status!")

        
    def on_enter(self, widget):
        self._status_image.show()
    
   
    @property
    def request_context_identifier(self):
        return self._request_context_id 
   
   
    @request_context_identifier.setter
    def request_context_identifier(self, value):
        self._request_context_id = value
        
        
    @property
    def file_path(self):
        return self._file_path


    @file_path.setter
    def file_path(self, value):
        self._file_path = value


    @property
    def file_name(self):
        return self._name_label.get_text()


    @file_name.setter
    def file_name(self, value):
        self._name_label.set_text(value)


    @property
    def file_type(self):
        return self._type_label.get_text()


    @file_type.setter
    def file_type(self, value):
        self._type_label.set_text(value)


    @file_type.setter
    def file_type(self, value):
        self._type_label.set_text(value)


