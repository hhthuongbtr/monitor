from DAL.api_agent import Agent as ApiAgentDAL
from DAL.database_agent import Agent as DbAgentDAL
from config import config

class Agent:
    def __init__(self):
        self.master_api = ApiAgentDAL(config.MATSER_API)
    def put(self, data):
        http_master_rsp = self.master_api.put(data)
        if http_master_rsp["status"] == 202:
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"

        if config.DEFINE_SLAVE_API:
            slave_api = ApiAgentDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.put(data)
            if http_slave_rsp["status"] == 202:
                print eror
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbAgentDAL()
            db_rsp = master_db.put(data)
            if db_rsp["status"] == 202:
                print eror
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
        print eror
        return http_master_rsp

