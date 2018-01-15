from DAL.api_profile import Profile as ApiProfileDAL
from DAL.api_profile import Snmp as ApiSnmpDAL
from DAL.database_profile import Profile as DbProfileDAL
from DAL.database_profile import Snmp as DbSnmpDAL
from config import config

class Profile:
    def __init__(self):
        self.master_api = ApiProfileDAL(config.MATSER_API)

    def get(self):
        http_master_rsp = self.master_api.get()
        if http_master_rsp["status"] == 200:
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"

        if config.DEFINE_SLAVE_API:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get()
            if http_slave_rsp["status"] == 200:
                print eror
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbProfileDAL()
            db_rsp = master_db.get()
            if db_rsp["status"] == 200:
                print eror
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
        print eror
        return http_master_rsp

    def put(self, id, data):
        http_master_rsp = self.master_api.put(id, data)
        if http_master_rsp["status"] == 202:
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"

        if config.DEFINE_SLAVE_API:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.put(id, data)
            if http_slave_rsp["status"] == 202:
                print eror
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbProfileDAL()
            db_rsp = master_db.put(id, data)
            if db_rsp["status"] == 202:
                print eror
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
        print eror
        return http_master_rsp

class Snmp:
    def __init__(self):
        self.master_api = ApiSnmpDAL(config.MATSER_API)

    def get(self):
        http_master_rsp = self.master_api.get()
        if http_master_rsp["status"] == 200:
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"

        if config.DEFINE_SLAVE_API:
            slave_api = ApiSnmpDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get()
            if http_slave_rsp["status"] == 200:
                print eror
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbSnmpDAL()
            db_rsp = master_db.get()
            if db_rsp["status"] == 200:
                print eror
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
        print eror
        return http_master_rsp
