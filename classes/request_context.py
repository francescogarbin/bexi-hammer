import os
import sys
import json
from .request_context_event import RequestContextEvent
from .log import Log as log

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


class RequestContext:

    def create_from_json_file(endpoint_id, file_path):
        ctx = None
        try:
            with open(file_path, mode='r', encoding='utf-8') as json_file:
                json_dict = json.load(json_file)
            ctx = RequestContext(endpoint_id, json_dict, file_path)
        except Exception as jsonex:
            log.exception(jsonex)
            ctx = RequestContext.handle_malformed_JSON_exception(jsonex,
                                                                 endpoint_id,
                                                                 file_path)
        return ctx
        

    def handle_malformed_JSON_exception(ex, endpoint_id, file_path):
        ctx = RequestContext(endpoint_id, None, file_path)
        ctx.status = RequestContextStatus.Error
        with open(file_path) as f:
            content = f.read()
        ctx.add_error_event(str(ex), content)
        return ctx 


    def build_identier(file_path):
        return os.path.basename(file_path)
        
        
    def __init__(self, endpoint_id, json_dict, file_path):
        self._endpoint_id = endpoint_id
        self._identifier = RequestContext.build_identier(file_path)
        self._status = RequestContextStatus.Idle
        self._file_path = file_path
        self._json_body = json_dict
        self._events = []
        

    @property
    def endpoint_identifier(self):
        return self._endpoint_id
        
        
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
        try:
            return json.dumps(self._json_body)
        except Exception as e:
            return {}
 
 
    @property
    def text(self):
        return json.dumps(self._json_body, ensure_ascii=False)


    @property
    def pretty_text(self):
        ret = None
        try:
            ret = json.dumps(self._json_body,
                             indent=4,
                             sort_keys=False,
                             ensure_ascii=False)
        except Exception as e:
            ret = ""
        return ret

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
        
        
    def add_completion_event(self, title, description, json_trace):
        self.status = RequestContextStatus.Completed
        outcome = self._find_key_value(json.loads(json_trace),
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
        event.trace = json_trace
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

    
    def reload(self):
        ctx = None
        try:
            with open(self._file_path) as json_file:
                json_dict = json.load(json_file)
            ctx = RequestContext(self._endpoint_id, json_dict, self._file_path)
        except Exception as jsonex:
            log.exception(jsonex)
            ctx = RequestContext.handle_malformed_JSON_exception(jsonex,
                                                            self._endpoint_id,
                                                            self._file_path)
        return ctx
               
               
    def _find_key_value(self, json_dict, key):        
        results = self._find_key_values(json_dict, key)
        if len(results) > 0:
            return results[0]
        return None

    
    def _find_key_values(self, json_dict, key):
        results = []
        try:
            def _decode_dict(a_dict):
                try:
                    results.append(a_dict[key])
                except KeyError:
                    pass
                return a_dict
            if self._json_body:
                raw_json = json.dumps(json_dict)
                json.loads(raw_json, object_hook=_decode_dict)
        except Exception as e:
            log.error("Exception in RequestContext._find_key_values")
            log.exception(e)
        return results

