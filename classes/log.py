import os
import sys
import logging
import appdirs

class Log:
    """ Factory del logger globale. L'istanza viene creata, se non presente,
        alla prima chiamata log.debug(), log.info(), etc.
        Il file di log viene creato nella directory dedicata al logging,
        su Linux questa è /home/user/.cache/bexi-hammer. Per altri sistemi
        operativi si veda il package Python appdirs che documenta le posizioni
        dei log file sui diversi sistemi operativi.
    """

    APPNAME = "bexi-hammer"
    AUTHOR = "blucrm" 
    LEVEL = logging.DEBUG
    
    _logger = None
    
    @staticmethod
    def debug(value):
        Log.get_log().debug(value)
    
    
    @staticmethod
    def info(value):
        Log.get_log().debug(value)
    
    
    @staticmethod
    def warn(value):
        Log.get_log().debug(value)
    
    
    @staticmethod
    def error(value):
        Log.get_log().debug(value)
    
    
    @staticmethod
    def get_log():
        if not Log._logger:
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            path = appdirs.user_log_dir(Log.APPNAME, Log.AUTHOR)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            hdlr = logging.FileHandler(path)
            hdlr.setFormatter(formatter)
            Log._logger = logging.getLogger(Log.APPNAME)
            Log._logger.setLevel(Log.LEVEL)
            Log._logger.addHandler(hdlr)
            Log._logger.addHandler(logging.StreamHandler(sys.stdout))

        return Log._logger
