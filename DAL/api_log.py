from api_monitor import ApiMonitor

class Log:
    def __init__(self, api):
        self.api = ApiMonitor(api)
    def post(self, data):
        url = self.api.log_url
        rsp = self.api.post(url, data)
        return rsp

