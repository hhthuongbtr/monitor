from DAL.api_log import Log as ApiLogDAL
from DAL.database_log import Log as DbLogDAL
from config.config import DEFINE_DATABASE_BACKUP as is_backup

class Log:
    def __init__(self):
        self.log_api = ApiLogDAL()
        self.lod_db = DbLogDAL()
    def post(self, data):
        rsp = self.log_api.post(data)
        if rsp["status"] == 201:
            return rsp
        if is_backup:
            return self.lod_db.post(data)
        return rsp
