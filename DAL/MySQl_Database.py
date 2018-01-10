import MySQLdb as mdb
import json
import config

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
    INSERT, UPDATE, DELETE, CREATE, and SET statement
    '''
    def execute_non_query(self, query):
        if not query:
            print 'No query!'
            return 0
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            session.commit()
            self.close_connect(session)
            return 1
        except Exception as e:
            return 0

    '''SELECT'''
    def execute_query(self, query):
        if not query:
            print 'No query!'
            return 0
        try:
            session = self.connect()
            cur=session.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            self.close_connect(session)
            return rows
        except Exception as e:
            print e
            return 0

