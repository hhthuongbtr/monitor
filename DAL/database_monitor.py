import MySQLdb as mdb
from config.config import DATABASE

class Database:
    def __init__(self, database):
        self.db = DATABASE[database]["NAME"]
        self.user = DATABASE[database]["USER"]
        self.password = DATABASE[database]["PASSWORD"]
        self.host = DATABASE[database]["HOST"]
        self.port = DATABASE[database]["PORT"]

    def connect(self):
        return mdb.connect(host=self.host, port=self.port, user=self.user, passwd=self.password, db=self.db)

    def close_connect(self, session):
        return session.close()

    '''
    INSERT, UPDATE, DELETE, CREATE statement
    '''
    def execute_non_query(self, query):
        if not query:
            status = 1
            message = "No query"
            data = None
            return status, message, data
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            session.commit()
            self.close_connect(session)
            status = 0
            message = "Ok"
            data = None
            return status, message, data
        except Exception as e:
            status = 1
            message = str(e)
            data = None
            return status, message, data

    '''SELECT'''
    def execute_query(self, query):
        if not query:
            status = 1
            message = "No query"
            data = None
            return status, message, data
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            data_table = cur.fetchall()
            self.close_connect(session)
            status = 0
            message = "Ok"
            data = data_table
            return status, message, data
        except Exception as e:
            status = 1
            message = str(e)
            data = None
            return status, message, data
