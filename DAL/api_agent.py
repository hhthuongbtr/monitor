from api_monitor import ApiMonitor
from config.config import SYSTEM

class Agent:
    def __init__(self, api):
        self.api = ApiMonitor(api)
    def put(self, data):
        rsp = self.api.put(self.api.agent_url + SYSTEM["HOST"] + "/", data)
        return rsp

