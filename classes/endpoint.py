import os
from .request_context import RequestContext
from .log import Log as log


class Endpoint:
    
    def __init__(self, identifier):
        self._identifier = identifier
        self._requests = None
        self._requests_files_path = None
        self._token_url = None
        self._adapter_url = None
        self._credentials = None
        self._visible_name = None

    @property
    def requests(self):
        return self._requests

    @requests.setter
    def requests(self, value):
        self._requests = value

    @property
    def identifier(self):
        return self._identifier
    
    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def requests_files_path(self):
        return self._requests_files_path

    @requests_files_path.setter
    def requests_files_path(self, value):
        self._requests_files_path = value

    @property
    def token_url(self):
        return self._token_url

    @token_url.setter
    def token_url(self, value):
        self._token_url = value

    @property
    def adapter_url(self):
        return self._adapter_url

    @adapter_url.setter
    def adapter_url(self, value):
        self._adapter_url = value

    @property
    def credentials(self):
        return self._credentials

    @credentials.setter
    def credentials(self, value):
        self._credentials = value
    
    @property
    def visible_name(self):
        return self._visible_name
    
    @visible_name.setter
    def visible_name(self, value):
        self._visible_name = value

    def add_new_request_context(self):
        default_json = { "Nuova richiesta":"Hey, compila con JSON valido" }
        file_path = self._get_first_available_file_path()
        ctx = RequestContext(self._identifier, default_json, file_path)
        self._requests[ctx.identifier] = ctx
        return ctx

    def _get_first_available_file_path(self):
        counter = 1
        while True:
            file_name = "Senza titolo {}.json".format(counter)
            file_path = os.path.join(self._requests_files_path, file_name)
            if self._get_request_by_file_path(file_path) is not None:
                counter += 1
            else:
                break
        return file_path

    def _get_request_by_file_path(self, file_path):
        for request_context in self._requests.values():
            if request_context.file_path == file_path:
                return request_context
        return None

