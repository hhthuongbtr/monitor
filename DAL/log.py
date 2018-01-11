from api_monitor import ApiMonitor

class Log:
    def __init__(self):
        self.api = ApiMonitor()
    def post(self, data):
    	url = self.api.log_url
    	print url
        rsp = self.api.post(url, data)
        return rsp

