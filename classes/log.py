class LogLevel:
    
    Debug = 0
    Info = 1
    Warn = 2
    Error = 3

class Log:

    _log = None
    
    @staticmethod
    def debug(value):
        Log._get_log()._log_impl(value)

    
    @staticmethod
    def info(value):
        Log._get_log()._log_impl(value)
    
    
    @staticmethod
    def warn(value):
        Log._get_log()._log_impl(value)
        
        
    @staticmethod
    def error(value):
        Log._get_log()._log_impl(value)
    
    @staticmethod
    def _get_log():
        if None == Log._log:
            Log._log = Log(LogLevel.Debug)
        return Log._log

    
    def __init__(self, log_level):
        self._log_level = log_level

    
    def _log_impl(self, value):
        print(value)
        
        
