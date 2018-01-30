import logging
from DAL.api_profile import Profile as ApiProfileDAL
from DAL.api_profile import Snmp as ApiSnmpDAL
from DAL.database_profile import Profile as DbProfileDAL
from DAL.database_profile import Snmp as DbSnmpDAL
from config import config

class Profile(object):
    """docstring for Profile"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.master_api = ApiProfileDAL(config.MASTER_API)

    def get(self):
        http_master_rsp = self.master_api.get()
        if http_master_rsp["status"] == 200:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if config.DEFINE_SLAVE_API:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get()
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbProfileDAL()
            db_rsp = master_db.get()
            if db_rsp["status"] == 200:
                self.logger.info("Database: " + db_rsp["message"])
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
                self.logger.warning("Database: " + db_rsp["message"])
        print eror
        self.logger.error(eror)
        return http_master_rsp
        
    def get_video_check_list(self):
        http_master_rsp = self.master_api.get_video_check_list()
        if http_master_rsp["status"] == 200:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if config.DEFINE_SLAVE_API:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get_video_check_list()
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbProfileDAL()
            db_rsp = master_db.get_video_check_list()
            if db_rsp["status"] == 200:
                self.logger.info("Database: " + db_rsp["message"])
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
                self.logger.warning("Database: " + db_rsp["message"])
        print eror
        self.logger.error(eror)
        return http_master_rsp

    def put(self, id, data):
        http_master_rsp = self.master_api.put(id, data)
        if http_master_rsp["status"] == 202:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if config.DEFINE_SLAVE_API:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.put(id, data)
            if http_slave_rsp["status"] == 202:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbProfileDAL()
            db_rsp = master_db.put(id, data)
            if db_rsp["status"] == 202:
                self.logger.info("Database: " + db_rsp["message"])
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
                self.logger.warning("Database: " + db_rsp["message"])
        print eror
        self.logger.error(eror)
        return http_master_rsp

class Snmp(object):
    """docstring for Snmp"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.master_api = ApiSnmpDAL(config.MASTER_API)

    def get(self):
        http_master_rsp = self.master_api.get()
        if http_master_rsp["status"] == 200:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if config.DEFINE_SLAVE_API:
            slave_api = ApiSnmpDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get()
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbSnmpDAL()
            db_rsp = master_db.get()
            if db_rsp["status"] == 200:
                self.logger.info("Database: " + db_rsp["message"])
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
                self.logger.warning("Database: " + db_rsp["message"])
        print eror
        self.logger.error(eror)
        return http_master_rsp
