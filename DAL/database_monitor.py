import MySQLdb as mdb
import json
from config import config

class Database:
    def connect(self):
        db = config.DATABASE_NAME
        user = config.DATABASE_USER
        password = config.DATABASE_PASSWORD
        host = config.DATABASE_HOST
        port = config.DATABASE_PORT
        return mdb.connect(host=host, port=port, user=user, passwd=password, db=db)

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
            status = 0
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
            return status, message, data_table
        except Exception as e:
            status = 1
            message = str(e)
            data = None
            return status, message, data

