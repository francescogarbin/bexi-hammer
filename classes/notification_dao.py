import pyodbc
from .log import Log
from .dao_base import DaoBase
from .notification_dao_value import NotificationDaoValue

class NotificationDao(DaoBase):

    def __init__(self):
        super().__init__()

    def get_150_by_request_id(self, request_id):
        pass

    def get_by_request_number(self, request_year, request_number, since):
        pass
