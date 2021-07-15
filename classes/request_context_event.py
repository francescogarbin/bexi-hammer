class RequestContextEvent:

    def __init__(self):
        self._title = None
        self._description = None
        self._trace = None


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

        
    def to_string(self):
        ret = ""
        if self._title:
            ret += "{}\n".format(self._title)
        if self._description:
            ret += "{}\n".format(self._description)
        if self._trace:
            ret += "{}\n".format(self._trace)
        return ret

