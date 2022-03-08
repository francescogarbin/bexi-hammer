import pytds
import pyodbc
from .log import Log as log
from .notification_dao_value import NotificationDaoValue


class DaoBase:

    Driver = "{FreeTDS}"
    Server = "" #indirizzo ip o simbolico del database server  
    Database = "" #nome del database blu_dispatcher_dati
    Username = "" #username dell'utente database con accesso in lettura al database
    Password = "=" #password dell'utente database
    
    def __init__(self):
        self.conn = None

    def open_connection(self):
        if self.conn is None:
            log.debug("Opening database connection to server {}...".format(self.Server))
            self.conn = pytds.connect(self.Server, self.Database, self.Username, self.Password, as_dict=True)
        
    def close_connection(self):
        if self.conn is not None:
            log.debug("Closing database connection to server {}...".format(self.Server))
            self.conn.close()
        self.conn = None

    def test_connection(self):
        self.open_connection()
        if self.conn is None:
            return False, "Connection is not open, open connection first.", None
        sql = ("select top 20 * from [IBex_Base].[BX_Msg] M"
               " order by M.InsertDt desc;")
        cursor = self.conn.cursor()
        cursor.execute(sql)
        values = []
        while 1:
            row = cursor.fetchone()
            if not row:
                break
            value = NotificationDaoValue()
            value.id_msg = row["IdMsg"]
            value.insert_dt = row["InsertDt"]
            value.xml_string = row["XmlString"]
            values.append(value)
            log.info(value.to_string())
        cursor.close()
        self.close_connection()
        return True, "Connection open, data fetch successful.", values
