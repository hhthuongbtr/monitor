from DAL.log import Log as LogDAL

class Log:
    def __init__(self):
        self.log = LogDAL()
    def post(self, data):
        return self.log.post(data)
