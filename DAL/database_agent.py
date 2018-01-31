import json
from config.config import SYSTEM
from database_monitor import Database

class Agent:
    def __init__(self, database):
        self.db = Database(database)

    def put(self, json_data):
        http_status_code = 500
        message = "Unknow"
        data = None
        if len(json_data)==3 and('cpu' and 'mem' and 'disk' in json_data):
            sql="update agent set cpu=%s,mem=%s,disk=%s,last_update=unix_timestamp() where ip='%s';"%(json_data['cpu'],json_data['mem'],json_data['disk'],SYSTEM["HOST"])
        else:
            http_status_code = 500
            message = "Only acept fields: cpu, mem, disk"
            data = None
            status = -1
        status, message, data_table = self.db.execute_non_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = None
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

