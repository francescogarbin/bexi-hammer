import os
import sys
import json
import threading
import logging
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject
from .log import Log as log
from .file_row import FileRow
from .source_view import SourceView
from .helpers import Helpers
from .bexi_adapter import BEXiAdapter
from .request_context import RequestContext
from .request_context import RequestContextEvent
from .request_context import RequestContextStatus
from .endpoint import Endpoint

log = logging.getLogger('bexi-hammer')
hdlr = logging.FileHandler('bexi-hammer.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)

@Gtk.Template(filename="resources/main_window_v1.ui")
class MainWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "main_window"

    statusbar = Gtk.Template.Child('statusbar')
    refresh_files_button = Gtk.Template.Child('refresh_files_button')
    files_scrollwindow = Gtk.Template.Child('files_scrollwindow')
    files_listbox = Gtk.Template.Child('files_listbox')
    page_1_box = Gtk.Template.Child('page_1_box')
    tmp_image = Gtk.Template.Child('tmp_image')
    headerbar_1 = Gtk.Template.Child('headerbar_1')
    headerbar_2 = Gtk.Template.Child('headerbar_2')
    main_stack = Gtk.Template.Child('main_stack')
    source_scrollview = Gtk.Template.Child('source_scrollview')
    files_status_label = Gtk.Template.Child('files_listbox_status_label')
    server_combo = Gtk.Template.Child('server_combo')
    filename_label = Gtk.Template.Child('filename_label')
    filepath_label = Gtk.Template.Child('filepath_label')
    adapter_url_label = Gtk.Template.Child('adapter_url_label')
    token_url_label = Gtk.Template.Child('token_url_label')
    file_open_button = Gtk.Template.Child('file_open_button')
    dir_open_button = Gtk.Template.Child('dir_open_button')
    save_as_button = Gtk.Template.Child('file_save_as_button')
    run_button = Gtk.Template.Child('run_button')
    pause_button = Gtk.Template.Child('pause_button')
    stop_button = Gtk.Template.Child('stop_button')
    reset_button = Gtk.Template.Child('reset_button')
    settings_button = Gtk.Template.Child('settings_button')
    about_button = Gtk.Template.Child('about_button')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = self.app.get_settings()
        if not settings:
            self._show_alert_dialog("Impostazioni non trovate",
                        "L'applicazione non trova le impostazioni, assicurati"\
                        " che il file di impostazioni sia presente.")
        endpoint_id = settings.get_default_endpoint_id()
        combo_model = settings.get_endpoints_list_store()
                               
        self.files_listbox.connect("row-selected", self.on_row_selected)
        self.refresh_files_button.connect("clicked", self.on_refresh_files)        
        
        self.source_view = SourceView()
        self.source_scrollview.add(self.source_view.view)
        
        self.page_1_box.show()
        self.main_stack.show()

        renderer_text = Gtk.CellRendererText()
        self.server_combo.pack_start(renderer_text, True)
        self.server_combo.add_attribute(renderer_text, "text", 1)
        self.server_combo.set_id_column(0)
        self.server_combo.set_model(combo_model)
        self.server_combo.set_active_id(endpoint_id)
        self.server_combo.connect("changed", self.on_endpoint_changed)
        
        self.file_open_button.connect("clicked", self.on_file_open)
        self.dir_open_button.connect("clicked", self.on_dir_open)
        self.save_as_button.connect("clicked", self.on_file_save_as)
        self.run_button.connect("clicked", self.on_run_request)
        self.pause_button.connect("clicked", self.on_pause_request)
        self.stop_button.connect("clicked", self.on_stop_request)
        self.reset_button.connect("clicked", self.on_reset_request)
        self.settings_button.connect("clicked", self.on_settings)
        self.about_button.connect("clicked", self.on_about)
        
        self._refresh_files_listbox(endpoint_id)
        self._set_stock_status_text("environment_ready")
        self.files_listbox.show()
        self.show_all()
        self._hide_files_listbox_statuses()
        
    @property
    def app(self):
        return self.get_application()

    def on_dir_open(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        if not endpoint_id:
            self._show_alert_dialog(
                        "Nessun ambiente selezionato",
                        "Prima di caricare un file, seleziona un"\
                        " ambiente in cui caricare il tracciato della richiesta.")
            return
        dialog = Gtk.FileChooserDialog(title="Seleziona una cartella",
                                       parent=self,
                                       action=Gtk.FileChooserAction.SELECT_FOLDER)
        dialog.set_local_only(False)
        dialog.add_buttons(Gtk.STOCK_CANCEL,
                           Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_APPLY,
                           Gtk.ResponseType.OK)                           
        response = dialog.run()
        path = None
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
        dialog.destroy()
        duplicates_skipped = False
        if path:
            requests = self.app.get_request_contexts(endpoint_id)
            files = os.listdir(path)
            for file_name in files:
                if file_name.lower().endswith(".json"):
                    file_path = os.path.join(path, file_name)
                    if not RequestContext.build_identier(file_path) in requests:
                        ctx = self.app.add_request_context_from_file(endpoint_id,
                                                                file_path)
                        row = FileRow.create_from_request_context(ctx)
                        self.files_listbox.add(row)
                        self.files_listbox.select_row(row)
                        row.show()
                        row.grab_focus()
                    else:
                        duplicates_skipped = True
        if duplicates_skipped:
            self._show_alert_dialog(
                    "Alcuni file erano dei duplicati",
                    "Alcuni dei file presenti nella directory avevano lo"\
                    " stesso nome di file di richiesta già caricati in"\
                    " e sono stati ignorati.")
            

    def on_file_save_as(self, widget):
        dialog = Gtk.FileChooserDialog(title="Seleziona un file",
                                       parent=self,
                                       action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL,
                           Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_SAVE,
                           Gtk.ResponseType.OK)
        dialog.set_current_name("Untitled.txt")
        dialog.set_do_overwrite_confirmation(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
        dialog.destroy()
        with open(file_path, "w") as text_file:
            text_file.write(self.source_view.text)


    def on_file_open(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        if not endpoint_id:
            self._show_alert_dialog(
                        "Nessun ambiente selezionato",
                        "Prima di caricare un file, seleziona un"\
                        " ambiente in cui caricare il tracciato della richiesta.")
            return
        dialog = Gtk.FileChooserDialog(title="Please choose a file",
                                       parent=self,
                                       action=Gtk.FileChooserAction.OPEN)
        dialog.add_buttons(Gtk.STOCK_CANCEL,
                           Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_OPEN,
                           Gtk.ResponseType.OK)                           
        filter_json = Gtk.FileFilter()
        filter_json.set_name("File JSON")
        filter_json.add_pattern("*.JSON")
        filter_json.add_pattern("*.Json")
        filter_json.add_pattern("*.json")
        dialog.add_filter(filter_json)
        response = dialog.run()
        file_path = None
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
        dialog.destroy()
        if file_path:
            requests = self.app.get_request_contexts(endpoint_id)
            if RequestContext.build_identier(file_path) in requests:
                self._show_alert_dialog(
                        "Il file esiste già",
                        "Una richiesta che proviene dallo stesso file"\
                        " è già presente nella lista delle richieste.")            
            else:
                ctx = self.app.add_request_context_from_file(endpoint_id,
                                                             file_path)
                row = FileRow.create_from_request_context(ctx)
                self.files_listbox.add(row)
                self.files_listbox.select_row(row)
                row.show()
            

    def on_file_save_as(self, widget):
        dialog = Gtk.FileChooserDialog(title="Please choose a file",
                                       parent=self,
                                       action=Gtk.FileChooserAction.SAVE)
        dialog.add_buttons(Gtk.STOCK_CANCEL,
                           Gtk.ResponseType.CANCEL,
                           Gtk.STOCK_SAVE,
                           Gtk.ResponseType.OK)
        dialog.set_current_name("Untitled.txt")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_path = dialog.get_filename()
        dialog.destroy()
        with open(file_path, "w") as text_file:
            text_file.write(self.source_view.text)
        

    def on_run_request(self, widget):
        log.debug("on_run_request()...")
        try:
            endpoint_id = self.server_combo.get_active_id()
            row = self.files_listbox.get_selected_row()
            ctx_id = row.request_context_identifier
            ctx = self.app.get_request_context(endpoint_id, ctx_id)
            ctx.thread = threading.Thread(target=self._post_request,
                                          args=(ctx, endpoint_id),
                                          daemon=True)
            ctx.thread.start()
        except Exception as e:
            self._handle_exception("Could not post request", e)      
        

    def on_pause_request(self, widget):
        log.debug("on_pause_request()...")


    def on_stop_request(self, widget):
        log.debug("on_stop_request()...")

        
    def on_reset_request(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        row = self.files_listbox.get_selected_row()
        ctx_id = row.request_context_identifier
        ctx = self.app.get_request_context(endpoint_id, ctx_id)
        ctx.reset()
        self.source_view.request_context = ctx
        self._set_files_listbox_row_status(ctx)
        self._inflect_request_context_status(ctx)
        
    
    def on_endpoint_changed(self, entry):
        self._refresh_files_listbox(entry.get_active_id())
    
        
    def on_row_selected(self, widget, row):
        if row:
            endpoint_id = self.server_combo.get_active_id()
            settings = self.app.get_settings()
            ctx_id = row.request_context_identifier
            ctx = self.app.get_request_context(endpoint_id, ctx_id)
            adapter_url = self.app.get_endpoint(endpoint_id).adapter_url
            token_url = self.app.get_endpoint(endpoint_id).token_url
            self.source_view.request_context = ctx
            self.filename_label.set_text(ctx.file_name)
            self.filepath_label.set_text(ctx.file_path)
            self.adapter_url_label.set_text(adapter_url)
            self.token_url_label.set_text(token_url)
            self._inflect_request_context_status(ctx)
                

    def on_refresh_files(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        self._refresh_files_listbox(endpoint_id)


    def on_settings(self, widget):
        log.debug("on_settings()...")

        
    def on_about(self,widget):
        about_dialog = Gtk.AboutDialog(transient_for=self, modal=True)
        about_dialog.present()

    
    def _set_status_text(self, text):
        context_id = self.statusbar.get_context_id("status") 
        self.statusbar.push(context_id, text)

    
    def _set_stock_status_text(self, stock_id):
        if "environment_ready":
            settings = self.app.get_settings()
            endpoint_id = self.server_combo.get_active_id()
            endpoint = settings.get_endpoint(endpoint_id)
            environment = endpoint["visible_name"]
            endpoint_url = endpoint["server_url"]
            text = "Current environment: {} at {}.".format(environment, endpoint_url)
            self._set_status_text(text)
        else:
            self._set_status_text("Ready")
        
        
    def _set_files_status_text(self, count):
        text = "{} available".format(Helpers.pluralize(count, "file", "files"))
        self.files_status_label.set_text(text)
        
        
    def _refresh_files_listbox(self, endpoint_id):
        self._inflect_request_context_status(None)
        contexts = self.app.get_endpoint(endpoint_id).requests
        for row in self.files_listbox.get_children():
            self.files_listbox.remove(row)
        for key, ctx in contexts.items():
            row = FileRow.create_from_request_context(ctx)
            self.files_listbox.add(row)
            row.show()
        if len(self.files_listbox) > 0:
            first_row = self.files_listbox.get_row_at_index(0)
            self.files_listbox.select_row(first_row)
        self._set_stock_status_text("environment_ready")        
        self._set_files_status_text(len(self.files_listbox))        
        
        
    def _hide_files_listbox_statuses(self):
        rows_count = len(self.files_listbox)
        for i in range(rows_count):
            row = self.files_listbox.get_row_at_index(i)
            row.hide_status()

    
    def _set_files_listbox_row_status(self, request_context):
        rows_count = len(self.files_listbox)
        for i in range(rows_count):
            row = self.files_listbox.get_row_at_index(i)
            if row.request_context_identifier == request_context.identifier:
                row.set_status_image(request_context.status)


    def _show_alert_dialog(self, title, message):
        dialog = Gtk.MessageDialog(parent=self,
                                   flags=Gtk.DialogFlags.MODAL,
                                   type=Gtk.MessageType.WARNING,
                                   buttons=Gtk.ButtonsType.OK,
                                   message_format=message)
        dialog.connect("response", self.on_alert_dialog_response)
        dialog.show()
        
        
    def on_alert_dialog_response(self, widget, response_id):
        widget.destroy()


    def _handle_exception(self, title, ex):
        message = getattr(ex, 'message', repr(ex))
        log.exception(ex);
        dialog = Gtk.MessageDialog(parent=self,
                                   flags=Gtk.DialogFlags.MODAL,
                                   type=Gtk.MessageType.ERROR,
                                   buttons=Gtk.ButtonsType.OK,
                                   message_format=message)
        dialog.connect("response", self._on_dialog_response)
        dialog.show()
        
        
    def _on_dialog_response(self, widget, response_id):
        widget.destroy()
        row = self.files_listbox.get_selected_row()
        if row:
            endpoint_id = self.server_combo.get_active_id()
            ctx_id = row.request_context_identifier
            ctx = self.app.get_request_context(endpoint_id, ctx_id)
            self._inflect_request_context_status(ctx)
        else:
            self._inflect_request_context_status(None)


    def _inflect_request_context_status(self, request_context):
        if None == request_context:
            self.run_button.set_sensitive(False)
            self.pause_button.set_sensitive(False)
            self.stop_button.set_sensitive(False)
        else:    
            self.run_button.set_sensitive(True)
            self.pause_button.set_sensitive(False)
            self.stop_button.set_sensitive(False)
            if RequestContextStatus.Idle == request_context.status:
                self.run_button.set_sensitive(True)
            elif RequestContextStatus.Running == request_context.status:
                self.pause_button.set_sensitive(True)
                self.stop_button.set_sensitive(True)
            elif RequestContextStatus.Completed == request_context.status:
                pass
            elif RequestContextStatus.Completed_NOT_OK == request_context.status:
                pass
            elif RequestContextStatus.Completed_WARN == request_context.status:
                pass
            elif RequestContextStatus.Error == request_context.status:
                pass
            elif RequestContextStatus.Undefined == request_context.status:
                pass
            else:
                raise Exception("Invalid request context status {}!"
                                             .format(request_context.status))
                

    def _append_event(self, request_context, event):
        row = self.files_listbox.get_selected_row()
        if row.request_context_identifier == request_context.identifier:
            self.source_view.append(event.get_source_text())


    def _post_request(self, request_context, endpoint_id):
        log.debug("post_request() entering...")
        try:
            if RequestContextStatus.Idle != request_context.status:
                log.warn("MainWindow._post_request() chiamata con richiesta in stato non Idle ({}.)".format(request_context.status))
                return
            request_context.status = RequestContextStatus.Running
            GLib.idle_add(self._inflect_request_context_status, request_context)
            GLib.idle_add(self._set_files_listbox_row_status, request_context)
            settings = self.app.get_settings()
            token_url = settings.get_endpoint_token_url(endpoint_id)
            credentials = settings.get_endpoint_credentials(endpoint_id)
            
            endpoint = self.app.get_endpoint(endpoint_id)
            credentials = self.app.get_endpoint(endpoint_id).credentials
            bexi = BEXiAdapter(endpoint.token_url, endpoint.adapter_url)
            
            event = request_context.add_log_event(
                                "GET token autenticazione...",
                                "Endpoint: {}...".format(endpoint.token_url))
            GLib.idle_add(self._append_event, request_context, event)
            
            event = request_context.add_log_event(
                                "Invio richiesta con method:POST...",
                                "Endpoint: {}".format(endpoint.adapter_url))
            GLib.idle_add(self._append_event, request_context, event)

            request_body = self.source_view.text
            response_json = bexi.post_request(credentials, request_body)
            if response_json:
                pretty = json.dumps(response_json, indent=4, sort_keys=False)
                event = request_context.add_completion_event(
                                    "Risposta ricevuta dal server",
                                    "Endpoint: {}".format(endpoint.adapter_url),
                                    pretty)
            else:
                event = request_context.add_error_event(
                                    "Nessuna risposta dal server!",
                                    "Endpoint: {}".format(endpoint.adapter_url))
            GLib.idle_add(self._append_event, request_context, event)
        except Exception as e:
            event = request_context.add_error_event(
                                "Nessuna risposta dal server!",
                                str(e))
            GLib.idle_add(self._append_event, request_context, event)
            log.warn("Exception raised in MainWindow._post_request()!")
            log.exception(e)                    
        finally:
            GLib.idle_add(self._inflect_request_context_status, request_context)
            GLib.idle_add(self._set_files_listbox_row_status, request_context)
            log.debug("post_request() leaving...")
        
        
