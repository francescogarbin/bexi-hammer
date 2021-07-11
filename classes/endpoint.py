import os, sys, json

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
    def requests(self, value):
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
    
    @requests.setter
    def visible_name(self, value):
        self._visible_name = value

    
