import time
from datetime import datetime

class RequestContextEvent:

    def __init__(self):
        self._title = None
        self._description = None
        self._trace = None
        self._timestamp = time.time()


    @property
    def title(self):
        if self._title:
            return self._title
        return ""
    
    @title.setter
    def title(self, value):
        self._title = value

        
    @property
    def description(self):
        if self._description:
            return self._description
        return ""
        

    @description.setter
    def description(self, value):
        self._description = value

        
    @property
    def trace(self):
        if self._trace:
            return self._trace
        return ""
        
    
    @trace.setter
    def trace(self, value):
        self._trace = value


    @property
    def timestamp(self):
        return self._timestamp
        
    
    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

