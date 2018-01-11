from DAL.api_agent import Agent as ApiAgentDAL
from DAL.database_agent import Agent as DbAgentDAL
from config.config import DEFINE_DATABASE_BACKUP as is_backup

class Agent:
    def __init__(self):
        self.agent_api = ApiAgentDAL()
        self.agent_db = DbAgentDAL()
    def put(self, data):
        rsp = self.agent_api.put(data)
        if rsp["status"] == 202:
            return rsp
        if is_backup:
            return self.agent_db.put(data)
        return rsp
