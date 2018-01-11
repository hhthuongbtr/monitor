from api_monitor import ApiMonitor
from config.config import IP as ip

class Profile:
    def __init__(self):
        self.api = ApiMonitor()

    def get(self):
        rsp = self.api.get(self.api.profile_agent_url + ip + "/")
        return rsp

    def put(self, id, data):
    	url = self.api.profile_agent_url + str(id) + "/"
    	print url
        rsp = self.api.put(url, data)
        return rsp

