from DAL.api_profile import Profile as ApiProfileDAL
from DAL.api_profile import Snmp as ApiSnmpDAL
from DAL.database_profile import Profile as DbProfileDAL
from DAL.database_profile import Snmp as DbSnmpDAL
from config.config import DEFINE_DATABASE_BACKUP as is_backup

class Profile:
    def __init__(self):
        self.profile_api = ApiProfileDAL()
        self.profile_db = DbProfileDAL()

    def get(self):
        rsp = self.profile_api.get()
        if rsp["status"] == 200:
            return rsp
        if is_backup:
            return self.profile_db.get()
        return rsp

    def put(self, id, data):
        rsp = self.profile_api.put(id, data)
        if rsp["status"] == 202:
            return self.profile_db.put(id, data)
        if is_backup:
            return self.profile_db.put(id, data)
        return rsp

class Snmp:
    def __init__(self):
        self.snmp_api = ApiSnmpDAL()
        self.snmp_db = DbSnmpDAL()
    def get(self):
        rsp = self.snmp_api.get()
        if rsp["status"] == 200:
            print "API"
            return rsp
        if is_backup:
            print "Database"
            return self.snmp_db.get()
        return rsp
