import logging
from DAL.api_agent import Agent as ApiAgentDAL
from DAL.database_agent import Agent as DbAgentDAL
from config import config

class Agent(object):
    """docstring for Agent"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.master_api = ApiAgentDAL(config.MASTER_API)
    def put(self, data):
        http_master_rsp = self.master_api.put(data)
        if http_master_rsp["status"] == 202:
            self.logger.info("Master Api: " + http_master_rsp["message"])
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"
        self.logger.warning("Master Api: " + http_master_rsp["message"])

        if config.DEFINE_SLAVE_API:
            slave_api = ApiAgentDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.put(data)
            if http_slave_rsp["status"] == 202:
                self.logger.info("Slave Api: " + http_slave_rsp["message"])
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"
                self.logger.warning("Slave Api: " + http_slave_rsp["message"])

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbAgentDAL()
            db_rsp = master_db.put(data)
            if db_rsp["status"] == 202:
                self.logger.info("Database: " + db_rsp["message"])
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
                self.logger.warning("Database: " + db_rsp["message"])
        self.logger.error(eror)
        return http_master_rsp

