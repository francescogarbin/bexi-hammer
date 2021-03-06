import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gio, Gtk
from classes.main_window import MainWindow
from classes.settings import Settings
from classes.request_context import RequestContext
from classes.endpoint import Endpoint
from classes.log import Log as log


class Application(Gtk.Application):

    ID = "org.blucrm.bexi-hammer"
    NAME = "bexi-hammer"
    VISIBLE_NAME = "BEXi Hammer"
    VERSION = "1.3 20210805 09:00"
    VISIBLE_VERSION = "1.3"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,
                         application_id=Application.ID,
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None
        self.add_main_option("test",
                             ord("t"),
                             GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE,
                             "Command line test",
                             None)
        self._settings = self._load_settings()
        if self._settings:
            self._endpoints = self.load_endpoints(self._settings)
        log.info("Applicazione avviata")

    def reload_endpoints(self):
        self._endpoints = self.load_endpoints(self._settings)

    def load_endpoints(self, settings):
        endpoints = {}
        s = settings
        ids = settings.get_endpoint_ids()
        for id in ids:
            e = Endpoint(id)
            e.requests = self.load_requests(id) 
            e.requests_files_path = settings.get_endpoint_requests_path(id)
            e.token_url = settings.get_endpoint_token_url(id)
            e.adapter_url = settings.get_endpoint_adapter_url(id)
            e.credentials = settings.get_endpoint_credentials(id)
            endpoints[id] = e
        return endpoints

    def reload_endpoint_requests(self, endpoint_id):
        self._endpoints[endpoint_id].requests = self.load_requests(endpoint_id) 

    def reload_endpoint_request(self, endpoint_id, request_context_id):
        old_ctx = self._endpoints[endpoint_id].requests[request_context_id]
        ctx = old_ctx.reload()
        self._endpoints[endpoint_id].requests[ctx.identifier] = ctx 
        return ctx

    def swap_endpoint_request(self, endpoint_id, old_ctx_id, new_ctx_file_path):
        endpoint = self._endpoints[endpoint_id]
        endpoint.requests.pop(old_ctx_id)
        ctx = self.add_request_context_from_file(endpoint_id, new_ctx_file_path)
        return ctx

    def add_request_context_from_file(self, endpoint_id, file_path):
        ctx = RequestContext.create_from_json_file(endpoint_id, file_path)
        self._endpoints[endpoint_id].requests[ctx.identifier] = ctx
        return ctx

    def get_endpoints(self):
        return self._endpoints

    def get_endpoint(self, endpoint_id):
        if endpoint_id in self._endpoints:
            return self._endpoints[endpoint_id]
        return None

    def get_request_contexts(self, endpoint_id):
        if endpoint_id in self._endpoints:        
            return self._endpoints[endpoint_id].requests
        return None

    def get_request_context(self, endpoint_id, request_context_id):
        if endpoint_id in self._endpoints:
            if request_context_id in self._endpoints[endpoint_id].requests:
                endpoint = self._endpoints[endpoint_id]
                return endpoint.requests[request_context_id]
        return None

    def get_settings(self):
        if None == self._settings:
            self._settings = self._load_settings() 
        return self._settings

    def _load_settings(self):
        if not Settings.settings_file_exists():
            Settings.create_settings_file()
        return Settings()

    def load_requests(self, endpoint_id):
        contexts = {}
        path = self._settings.get_endpoint_requests_path(endpoint_id)
        files = sorted(os.listdir(path))
        for file_name in files:
            if file_name.lower().endswith(".json"):
                file_path = os.path.join(path, file_name)
                ctx = RequestContext.create_from_json_file(endpoint_id,
                                                           file_path)
                contexts[ctx.identifier] = ctx
        return contexts

    def do_startup(self):
        Gtk.Application.do_startup(self)
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)
        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        if not self.window:
            self.window = MainWindow(application=self,
                          title=Application.VISIBLE_NAME)
            self.window.resize(1024, 768)
        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        if "test" in options:
            print("Argomento di test ricevuto: %s" % options["test"])
        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window,
                                       modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()

