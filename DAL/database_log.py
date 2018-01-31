import json
from database_monitor import Database

class Log:
    def __init__(self, database):
        self.db = Database(database)

    def post(self, json_data):
        http_status_code = 500
        message = "Unknow"
        data = None
        try:
            host = json_data['host']
            tag = json_data['tag']
            msg = json_data['msg']
        except:
            http_status_code = 500
            message = "Only acept fields: host, tag, msg"
            data = None
            json_response = {"status": http_status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            json_response = json.loads(json_response)
            return json_response
        sql="insert into logs(host,tag,datetime,msg) values('%s','%s', NOW(),'%s');"%(host, tag, msg)
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

