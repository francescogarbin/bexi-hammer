import json
import gi
from pathlib import Path
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from .endpoint import Endpoint


class Settings:

    _default_path = "data/settings.json"
    
    @staticmethod
    def create_settings_file():
        dict = {}
        endpoint = {}
        endpoint["identifier"] = "dummy"
        endpoint["visible_name"] = "Imposta {}".format(Settings._default_path)
        endpoint["requests_files_path"] = "."
        endpoint["server_url"] = "https://tuoserver.com"
        endpoint["token_route"] = "token"
        endpoint["adapter_route"] = "bexiadapter/startnewtask"
        endpoint["credentials"] = {}
        endpoint["credentials"]["username"] = "username"
        endpoint["credentials"]["password"] = "username"
        endpoint["credentials"]["client_secret"] = "client_secret"
        endpoint["credentials"]["client_id"] = "client_id"
        endpoint["credentials"]["scope"] = "scope"
        endpoint["credentials"]["grant_type"] = "grant_type"
        dict["version"] = "1.0"
        dict["endpoints"] = [endpoint]
        json_text = json.dumps(dict, indent=4, sort_keys=False)
        with open(Settings._default_path, "w") as text_file:
            text_file.write(json_text)


    @staticmethod
    def settings_file_exists():
        settings_file = Path(Settings._default_path)
        return settings_file.is_file()


    def __init__(self):
        self._settings = None
        if self.settings_file_exists():
            with open(self._default_path) as json_file:
                self._settings = json.load(json_file)


    def get_endpoints(self):
        endpoints = []
        if self._settings:
            for endpoint in self._settings["endpoints"]:
                endpoints.append(endpoint)
        return endpoints


    def get_endpoint_ids(self):
        ids = []
        if self._settings:
            for endpoint in self._settings["endpoints"]:
                ids.append(endpoint["identifier"])
        return ids


    def get_endpoints_list_store(self):
        ret = Gtk.ListStore(str, str)
        if self._settings:
            for endpoint in self._settings["endpoints"]:
                ret.append([endpoint["identifier"], endpoint["visible_name"]])
        return ret


    def get_endpoint(self, endpoint_identifier):
        if self._settings:
            for endpoint in self._settings["endpoints"]:
                if endpoint["identifier"] == endpoint_identifier:
                    return endpoint
        return None
        
        
    def get_endpoint_visible_name(self, endpoint_identifier):
        return self._get_endpoint_attribute(endpoint_identifier, "visible_name")


    def get_default_endpoint_id(self):
        ids = self.get_endpoint_ids()
        if len(ids) > 0:
            return ids[0]
        return None


    def get_endpoint_token_url(self, endpoint_identifier):
        server = self.get_endpoint(endpoint_identifier)
        if server:
            return server["server_url"] + "/" + server["token_route"]
        return None


    def get_endpoint_adapter_url(self, endpoint_identifier):
        server = self.get_endpoint(endpoint_identifier)
        if server:
            return server["server_url"] + "/" + server["adapter_route"]
        return None
    
    
    def get_endpoint_requests_path(self, endpoint_identifier):
        return self._get_endpoint_attribute(endpoint_identifier, "requests_files_path")

        
    def get_endpoint_credentials(self, endpoint_identifier):
        return self._get_endpoint_attribute(endpoint_identifier, "credentials")

    
    def _get_endpoint_attribute(self, endpoint_identifier, attribute_name):
        endpoint = self.get_endpoint(endpoint_identifier)
        if endpoint:
            return endpoint[attribute_name]
        return None
    
