from .log import Log

class NotificationDaoValue:

    def __init__(self):
        self.id_msg = None
        self.xml_string = None
        self.insert_dt = None
    
    def to_string(self):
        return "{}, {}, {}".format(self.id_msg,
                                   self.insert_dt,
                                   self.xml_string)

