from api_monitor import ApiMonitor
from config.config import SYSTEM

class Profile:
    def __init__(self, api):
        self.api = ApiMonitor(api)

    def get(self):
        rsp = self.api.get(self.api.profile_agent_url + SYSTEM["HOST"] + "/")
        return rsp

    def get_by_ip_multicast(self, source):
        rsp = self.api.get(self.api.agent_url + SYSTEM["HOST"] + "/" + source + "/")
        return rsp

    def get_video_check_list(self):
        rsp = self.api.get(self.api.video_check_url + SYSTEM["HOST"] + "/")
        return rsp
        
    def get_profile_id(self):
        rsp = self.api.get(self.api.video_check_url + SYSTEM["HOST"] + "/")
        return rsp

    def put(self, id, data):
        url = self.api.profile_agent_url + str(id) + "/"
        rsp = self.api.put(url, data)
        return rsp

class Snmp:
    def __init__(self, api):
        self.api = ApiMonitor(api)
    def get(self):
        rsp = self.api.get(self.api.snmp_url + SYSTEM["HOST"] + "/")
        return rsp