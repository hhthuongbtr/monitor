from api_monitor import ApiMonitor
from config.config import IP as ip

class Profile:
    def __init__(self, api_url):
        self.api = ApiMonitor(api_url)

    def get(self):
        rsp = self.api.get(self.api.profile_agent_url + ip + "/")
        return rsp

    def get_video_check_list(self):
        rsp = self.api.get(self.api.video_check_url)
        return rsp

    def put(self, id, data):
        url = self.api.profile_agent_url + str(id) + "/"
        rsp = self.api.put(url, data)
        return rsp

class Snmp:
    def __init__(self, api_url):
        self.api = ApiMonitor(api_url)
    def get(self):
        rsp = self.api.get(self.api.snmp_url)
        return rsp