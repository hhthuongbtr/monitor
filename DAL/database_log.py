import json
from database_monitor import Database

class Log:
    def __init__(self):
        self.db = Database()

    def post(self, json_data):
        http_status_code = 500
        message = "Unknow"
        data = None
        if len(json_data) == 3 and ('host' and 'tag' and 'msg' in json_data):
            sql="insert into logs(host,tag,datetime,msg) values('%s','%s', NOW(),'%s');"%(json_data['host'],json_data['tag'],json_data['msg'])
        else:
            http_status_code = 500
            message = "Only acept fields: host, tag, msg"
            data = None
            status = -1
        status, message, data_table = self.db.execute_non_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 201
            message = message
            data = data_table
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

