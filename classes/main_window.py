import os
import json
import threading
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GLib
from .file_row import FileRow
from .source_view import SourceView
from .helpers import Helpers
from .bexi_adapter import BEXiAdapter
from .request_context import RequestContext
from .request_context import RequestContextStatus
from .log import Log as log
from .log_view import LogView
from .settings_dialog import SettingsDialog
from .main_window_state import MainWindowState
from .dao_base import DaoBase
from .notification_dao import NotificationDao

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
    file_new_button = Gtk.Template.Child('file_new_button')
    file_open_button = Gtk.Template.Child('file_open_button')
    dir_open_button = Gtk.Template.Child('dir_open_button')
    save_button = Gtk.Template.Child('file_save_button')
    save_as_button = Gtk.Template.Child('file_save_as_button')
    run_button = Gtk.Template.Child('run_button')
    pause_button = Gtk.Template.Child('pause_button')
    stop_button = Gtk.Template.Child('stop_button')
    reset_button = Gtk.Template.Child('reset_button')
    settings_button = Gtk.Template.Child('settings_button')
    about_button = Gtk.Template.Child('about_button')
    log_textview = Gtk.Template.Child('log_textview')
    about_dialog = Gtk.Template.Child('about-dialog')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = MainWindowState(self)
        self.filename_label.set_text("Nessun file selezionato")
        self.filepath_label.set_text("--")
        self.token_url_label.set_text("--")
        self.adapter_url_label.set_text("--")
        settings = self.app.get_settings()
        if not settings:
            self._show_alert_dialog("Impostazioni non trovate",
                    "L'applicazione non trova le impostazioni, assicurati" \
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
        self.log_view = LogView(self.log_textview)
        self.file_new_button.connect("clicked", self.on_file_new)
        self.file_open_button.connect("clicked", self.on_file_open)
        self.dir_open_button.connect("clicked", self.on_dir_open)
        self.save_button.connect("clicked", self.on_file_save)
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
        #self._test_db_connection()
    
    @property
    def app(self):
        return self.get_application()

    def on_file_new(self, widget):
        try:
            endpoint_id = self.server_combo.get_active_id()
            endpoint = self.app.get_endpoint(endpoint_id)
            ctx = endpoint.add_new_request_context()
            row = FileRow.create_from_request_context(ctx)
            self.files_listbox.add(row)
            self.files_listbox.select_row(row)
            row.show()
        except Exception as e:
            self._handle_exception(e)
    
    def on_dir_open(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        if not endpoint_id:
            self._show_alert_dialog(
                "Nessun ambiente selezionato",
                "Prima di caricare un file, seleziona un" \
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
                    if RequestContext.build_identier(file_path) in requests:
                        duplicates_skipped = True
                    else:
                        ctx = self.app.add_request_context_from_file(
                            endpoint_id,
                            file_path)
                        row = FileRow.create_from_request_context(ctx)
                        self.files_listbox.add(row)
                        self.files_listbox.select_row(row)
                        row.show()
                        row.grab_focus()
        if duplicates_skipped:
            self._show_alert_dialog(
                "Alcuni file erano dei duplicati",
                "Alcuni dei file presenti nella directory avevano lo" \
                " stesso nome di file di richiesta già caricati in" \
                " e sono stati ignorati.")

    def on_file_open(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        if not endpoint_id:
            self._show_alert_dialog(
                "Nessun ambiente selezionato",
                "Prima di caricare un file, seleziona un ambiente" \
                " in cui caricare il tracciato della richiesta.")
            return
        dialog = Gtk.FileChooserDialog(title="Seleziona un file JSON",
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
                    "Una richiesta che proviene dallo stesso file" \
                    " è già presente nella lista delle richieste.")
            else:
                ctx = self.app.add_request_context_from_file(endpoint_id,
                                                             file_path)
                row = FileRow.create_from_request_context(ctx)
                self.files_listbox.add(row)
                self.files_listbox.select_row(row)
                row.show()

    def on_file_save(self, widget):
        try:
            endpoint_id = self.server_combo.get_active_id()
            ctx = self._get_selected_request_context()
            json_text = self.source_view.text
            RequestContext.validate_json_text(json_text)
            with open(ctx.file_path, mode="w", encoding="utf-8") as text_file:
                text_file.write(json_text)
            ctx = self.app.reload_endpoint_request(endpoint_id, ctx.identifier)
            self.source_view.set_request_context(ctx)
            self._set_files_listbox_row_status(ctx)
            self._inflect_request_context_status(ctx)
        except Exception as e:
            self._handle_exception(e)

    def on_file_save_as(self, widget):
        try:
            RequestContext.validate_json_text(self.source_view.text)
            dialog = Gtk.FileChooserDialog(title="Salva con nome",
                                           parent=self,
                                           action=Gtk.FileChooserAction.SAVE)
            dialog.add_buttons(Gtk.STOCK_CANCEL,
                               Gtk.ResponseType.CANCEL,
                               Gtk.STOCK_SAVE,
                               Gtk.ResponseType.OK)
            endpoint_id = self.server_combo.get_active_id()
            endpoint = self.app.get_endpoint(endpoint_id)
            dialog.set_current_folder(endpoint.requests_files_path)
            ctx = self._get_selected_request_context()
            dialog.set_current_name(ctx.file_name)
            dialog.set_do_overwrite_confirmation(True)
            response = dialog.run()
            file_path = None
            if response == Gtk.ResponseType.OK:
                file_path = dialog.get_filename()
            dialog.destroy()
            if file_path:
                with open(file_path, mode="w", encoding="utf-8") as text_file:
                    text_file.write(self.source_view.text)
                saved_ctx = self.app.add_request_context_from_file(endpoint_id,
                                                                   file_path)
                if not ctx.file_exists():
                    self._files_listbox_remove_request_context(ctx.identifier)
                    endpoint.requests.pop(ctx.identifier)
                row = FileRow.create_from_request_context(saved_ctx)
                self.files_listbox.add(row)
                self.files_listbox.select_row(row)
                row.show()
                self.source_view.set_request_context(saved_ctx)
                self._set_files_listbox_row_status(saved_ctx)
                self._inflect_request_context_status(saved_ctx)
        except Exception as e:
            self._handle_exception(e)

    def on_run_request(self, widget):
        try:
            endpoint_id = self.server_combo.get_active_id()
            row = self.files_listbox.get_selected_row()
            ctx_id = row.request_context_identifier
            ctx = self.app.get_request_context(endpoint_id, ctx_id)
            ctx.thread = threading.Thread(target=self._post_request,
                                          args=(ctx, endpoint_id),
                                          daemon=True)
            self.log_view.clear()
            ctx.thread.start()
        except Exception as e:
            self._handle_exception(e)

    def on_pause_request(self, widget):
        log.debug("MainWindow.on_pause_request() non ancora implementato.")

    def on_stop_request(self, widget):
        log.debug("MainWindow.on_stop_request() non ancora implementato.")

    def on_reset_request(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        row = self.files_listbox.get_selected_row()
        ctx_id = row.request_context_identifier
        ctx = self.app.get_request_context(endpoint_id, ctx_id)
        ctx.reset()
        self.source_view.set_request_context(ctx)
        self._set_files_listbox_row_status(ctx)
        self._inflect_request_context_status(ctx)
        self.log_view.clear()

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
            self.source_view.set_request_context(ctx)
            self.filename_label.set_text(ctx.file_name)
            self.filepath_label.set_text(ctx.file_path)
            self.adapter_url_label.set_text(adapter_url)
            self.token_url_label.set_text(token_url)
            self._inflect_request_context_status(ctx)
            self.log_view.append_request_context_events(ctx.events)

    def on_refresh_files(self, widget):
        endpoint_id = self.server_combo.get_active_id()
        self.app.reload_endpoint_requests(endpoint_id)
        self._refresh_files_listbox(endpoint_id)

    def on_settings(self, widget):
        settings_dialog = SettingsDialog()
        settings_dialog.run()

    def on_about(self, widget):
        self.about_dialog.show_all()
        self.about_dialog.run()
        self.about_dialog.hide()

    def _set_status_text(self, text):
        context_id = self.statusbar.get_context_id("status")
        self.statusbar.push(context_id, text)

    def _set_stock_status_text(self, stock_id):
        self._set_status_text("Pronto")
        if "environment_ready":
            settings = self.app.get_settings()
            endpoint_id = self.server_combo.get_active_id()
            endpoint = settings.get_endpoint(endpoint_id)
            environment = endpoint["visible_name"]
            endpoint_url = endpoint["server_url"]
            text = "Ambiente selezionato: {}, {}.".format(environment,
                                                          endpoint_url)
            self._set_status_text(text)

    def _set_files_status_text(self, count):
        text = "{}".format(Helpers.pluralize(count, "richiesta", "richieste"))
        self.files_status_label.set_text(text)

    def _refresh_files_listbox(self, endpoint_id):
        self._inflect_request_context_status(None)
        endpoint = self.app.get_endpoint(endpoint_id)
        contexts = endpoint.requests
        for row in self.files_listbox.get_children():
            self.files_listbox.remove(row)
        for key, ctx in contexts.items():
            row = FileRow.create_from_request_context(ctx)
            self.files_listbox.add(row)
            row.show()
        if len(self.files_listbox) > 0:
            first_row = self.files_listbox.get_row_at_index(0)
            self.files_listbox.select_row(first_row)
        self._set_stock_status_text("Ambiente Pronto")
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

    def _files_listbox_remove_request_context(self, request_context_id):
        for row in self.files_listbox.get_children():
            if row.request_context_identifier == request_context_id:
                self.files_listbox.remove(row)

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

    def _handle_exception(self, ex):
        message = getattr(ex, 'message', str(ex))
        log.exception(ex)
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

    def _inflect_request_context_status(self, ctx):
        if ctx is None:
            return
        row = self.files_listbox.get_selected_row()
        if row.request_context_identifier != ctx.identifier:
            return
        self.state.inflect(ctx.status)

    def _append_event(self, request_context, event):
        row = self.files_listbox.get_selected_row()
        if row.request_context_identifier == request_context.identifier:
            self.log_view.append_request_context_event(event)

    def _get_selected_request_context(self):
        endpoint_id = self.server_combo.get_active_id()
        row = self.files_listbox.get_selected_row()
        ctx_id = row.request_context_identifier
        ctx = self.app.get_request_context(endpoint_id, ctx_id)
        return ctx

    def _post_request(self, request_context, endpoint_id):
        try:
            request_context.status = RequestContextStatus.Running
            GLib.idle_add(self._inflect_request_context_status,
                          request_context)
            GLib.idle_add(self._set_files_listbox_row_status,
                          request_context)
            endpoint = self.app.get_endpoint(endpoint_id)
            bexi = BEXiAdapter(endpoint)
            event = request_context.add_log_event(
                "Invio richiesta GET token autenticazione...",
                "Endpoint: {}".format(endpoint.token_url))
            GLib.idle_add(self._append_event, request_context, event)
            token = bexi.get_token()
            event = request_context.add_completion_event(
                "Token di autenticazione ricevuto dal server",
                "Endpoint: {}".format(endpoint.token_url),
                json.dumps(token, indent=4, ensure_ascii=False))
            GLib.idle_add(self._append_event, request_context, event)
            event = request_context.add_log_event(
                "Invio richiesta POST a BEXi Adapter...",
                "Endpoint: {}".format(endpoint.adapter_url))
            GLib.idle_add(self._append_event, request_context, event)
            request_body = self.source_view.text.encode()
            outcome = bexi.start_new_task(token, request_body)
            outcome_json = json.dumps(outcome, indent=4, ensure_ascii=False)
            event = request_context.add_completion_event(
                "Risposta ricevuta dal server",
                "Endpoint: {}".format(endpoint.adapter_url),
                outcome_json)
            GLib.idle_add(self._append_event, request_context, event)
        except Exception as e:
            event = request_context.add_error_event(
                "Ooops, qualcosa è andato storto!",
                str(e))
            GLib.idle_add(self._append_event, request_context, event)
        finally:
            GLib.idle_add(self._inflect_request_context_status,
                          request_context)
            GLib.idle_add(self._set_files_listbox_row_status,
                          request_context)

    def _test_db_connection(self):
        dao = DaoBase()
        result, message, values = dao.test_connection()
        self._show_alert_dialog("Test di connessione al database", message)

