import logging
from DAL.api_log import Log as ApiLogDAL
from DAL.database_log import Log as DbLogDAL
from config import config

class Log(object):
    """docstring for Log"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.master_api = ApiLogDAL(config.MASTER_API)
    def post(self, data):
        http_master_rsp = self.master_api.post(data)
        if http_master_rsp["status"] == 201:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if config.DEFINE_SLAVE_API:
            slave_api = ApiLogDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.post(data)
            if http_slave_rsp["status"] == 201:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbLogDAL()
            db_rsp = master_db.post(data)
            if db_rsp["status"] == 201:
                self.logger.info("Database: " + db_rsp["message"])
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
                self.logger.warning("Database: " + db_rsp["message"])
        print eror
        self.logger.error(eror)
        return http_master_rsp

