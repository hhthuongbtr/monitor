from DAL.api_log import Log as ApiLogDAL
from DAL.database_log import Log as DbLogDAL
from config import config

class Log:
    def __init__(self):
        self.master_api = ApiLogDAL(config.MASTER_API)
    def post(self, data):
        http_master_rsp = self.master_api.post(data)
        if http_master_rsp["status"] == 201:
            return http_master_rsp
        eror = "Master Api: " + http_master_rsp["message"] + "\n"

        if config.DEFINE_SLAVE_API:
            slave_api = ApiLogDAL(config.SLAVE_API)
            http_slave_rsp = slave_api.post(data)
            if http_slave_rsp["status"] == 201:
                print eror
                return http_slave_rsp
            else:
                eror += "Slave Api: " + http_slave_rsp["message"] + "\n"

        if config.DEFINE_DATABASE_BACKUP:
            master_db = DbLogDAL()
            db_rsp = master_db.post(data)
            if db_rsp["status"] == 201:
                print eror
                return db_rsp
            else:
                eror += "Database: " + db_rsp["message"] + "\n"
        print eror
        return http_master_rsp

