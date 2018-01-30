from api_monitor import ApiMonitor

class Log:
    def __init__(self, api_url):
        self.api = ApiMonitor(api_url)
    def post(self, data):
        url = self.api.log_url
        rsp = self.api.post(url, data)
        return rsp

