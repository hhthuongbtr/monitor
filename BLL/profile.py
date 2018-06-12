import logging
from DAL.api_profile import Profile as ApiProfileDAL
from DAL.api_profile import Snmp as ApiSnmpDAL
from DAL.database_profile import Profile as DbProfileDAL
from DAL.database_profile import Snmp as DbSnmpDAL
from config.config import API, DATABASE

class Profile(object):
    """docstring for Profile"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.master_api = ApiProfileDAL("master")

    def get(self):
        http_master_rsp = self.master_api.get()
        if http_master_rsp["status"] == 200:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if API["slave"]["ACTIVE"]:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get()
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if DATABASE["master"]["ACTIVE"]:
            master_db = DbProfileDAL("master")
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

        if API["slave"]["ACTIVE"]:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get_video_check_list()
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if DATABASE["master"]["ACTIVE"]:
            master_db = DbProfileDAL("master")
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

        if API["slave"]["ACTIVE"]:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.put(id, data)
            if http_slave_rsp["status"] == 202:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if DATABASE["master"]["ACTIVE"]:
            master_db = DbProfileDAL("master")
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

    def get_by_ip_multicast(self, source):
        http_master_rsp = self.master_api.get_by_ip_multicast(source)
        if http_master_rsp["status"] == 200:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if API["slave"]["ACTIVE"]:
            slave_api = ApiProfileDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get_by_ip_multicast(source)
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if DATABASE["master"]["ACTIVE"]:
            master_db = DbProfileDAL("master")
            db_rsp = master_db.get_by_ip_multicast(source)
            if db_rsp["status"] == 200:
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
        self.master_api = ApiSnmpDAL("master")

    def get(self):
        http_master_rsp = self.master_api.get()
        if http_master_rsp["status"] == 200:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if API["slave"]["ACTIVE"]:
            slave_api = ApiSnmpDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.get()
            if http_slave_rsp["status"] == 200:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if DATABASE["master"]["ACTIVE"]:
            master_db = DbSnmpDAL("master")
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
