from api_monitor import ApiMonitor
from config.config import IP as ip

class Agent:
    def __init__(self, api_url):
        self.api = ApiMonitor(api_url)
    def put(self, data):
        rsp = self.api.put(self.api.agent_url + ip + "/", data)
        return rsp

