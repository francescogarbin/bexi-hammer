import os
import sys
import json

from classes.log import Log as log

class RequestOutcome:
    
    OutcomeLabel = "esito"
    Error = "0"
    Success = "1"
    Warn = "2"


class RequestContextStatus:

    Idle = 1
    Running = 2
    Paused = 3
    Completed = 4
    Completed_WARN = 5
    Completed_NOT_OK = 6
    Error = 7
    Undefined = 8

class RequestContextEvent:

    def __init__(self):
        self._title = None
        self._description = None
        self._log = None


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
    def log(self):
        if self._log:
            return self._log
        return ""
        
    
    @log.setter
    def log(self, value):
        self._log = value

        
    def get_source_text(self):
        return "#{}\n#{}\n{}\n".format(self.title, self.description, self.log)


class RequestContext:

    def create_from_json_file(endpoint_id, file_path):
        with open(file_path) as json_file:
            json_dict = json.load(json_file)
        return RequestContext(endpoint_id, json_dict, file_path)


    def build_identier(file_path):
        return os.path.basename(file_path)
        
        
    def __init__(self, endpoint_identifier, json_dict, file_path):
        self._endpoint_identifier = endpoint_identifier
        self._identifier = RequestContext.build_identier(file_path)
        self._status = RequestContextStatus.Idle
        self._file_path = file_path
        self._json_body = json_dict
        self._events = []
        

    @property
    def endpoint_identifier(self):
        return self._endpoint_identifier
        
        
    @property
    def identifier(self):
        return self._identifier
    
     
    @property
    def file_path(self):
        return self._file_path

    
    @property
    def file_name(self):
        ret = None
        if self._file_path:
            ret = os.path.basename(self._file_path)
        return ret


    @property
    def status(self):
        return self._status


    @status.setter
    def status(self, value):
        self._status = value

 
    @property
    def json_body(self):
        return json.dumps(self._json_body)
 
    @property
    def text(self):
        return json.dumps(self._json_body)


    @property
    def pretty_text(self):
        return json.dumps(self._json_body, indent=4, sort_keys=False)


    @property
    def events(self):
        return self._events
    
       
    @events.setter
    def events(self, value):
        self._events = value
    
    
    def add_log_event(self, title, description):
        event = RequestContextEvent()
        event.title = title
        event.description = description
        self.events.append(event)
        return event
        
        
    def add_completion_event(self, title, description, json_text):
        self.status = RequestContextStatus.Completed
        outcome = self._find_key_value(json.loads(json_text),
                                       RequestOutcome.OutcomeLabel)
        if RequestOutcome.Success == outcome:
            self.status = RequestContextStatus.Completed
        elif RequestOutcome.Warn == outcome:
            self.status = RequestContextStatus.Completed_WARN
        elif RequestOutcome.Error == outcome:
            self.status = RequestContextStatus.Completed_NOT_OK
        else:
            self.status = RequestContextStatus.Undefined
        event = RequestContextEvent()
        event.title = title
        event.description = description
        event.log = json_text
        self.events.append(event)
        return event
        

    def add_error_event(self, title, description):
        self.status = RequestContextStatus.Error
        event = RequestContextEvent()
        event.title = title
        event.description = description
        self.events.append(event)
        return event

    
    def get_attribute(self, name):
        value = self._find_key_value(self._json_body, name)
        if value:
            return value
        return "Non definito"

           
    def reset(self):
        self._events = []
        self.status = RequestContextStatus.Idle

    
    def _find_key_value(self, json_dict, key):        
        results = self._find_key_values(json_dict, key)
        if len(results) > 0:
            return results[0]
        return None

    
    def _find_key_values(self, json_dict, key):
        results = []
        def _decode_dict(a_dict):
            try:
                results.append(a_dict[key])
            except KeyError:
                pass
            return a_dict
        if self._json_body:
            raw_json = json.dumps(json_dict)
            json.loads(raw_json, object_hook=_decode_dict)
        return results
    
    

