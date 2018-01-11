import json
from config.config import IP as ip
from database_monitor import Database

class Profile:
    def __init__(self):
        self.db = Database()
    def parse_profile_data_table_to_json_array(self, profile_list):
        agent = {}
        args = []
        for profile in profile_list:
            args.append({ 
                            'id'            : profile[0] if profile[0] else None,
                            'ip'            : profile[1] if profile[1] else "",
                            'protocol'      : profile[2] if profile[2] else 'udp',
                            'status'        : profile[3] if profile[3] else 0,
                            'thread'        : profile[4] if profile[4] else 10,
                            'name'          : profile[5] if profile[5] else None,
                            'type'          : profile[6] if profile[6] else None
                        })
        agent["agent"] = args
        return agent

    def get(self):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = """select pa.id,p.ip,p.protocol,pa.status,a.thread,c.name,p.type
                from profile as p, agent as a, profile_agent as pa,channel as c 
                where a.ip='%s' and a.active=1 and pa.monitor=1 and p.channel_id=c.id and pa.profile_id=p.id and pa.agent_id=a.id"""%(ip)
        status, message, data_table = self.db.execute_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = self.parse_profile_data_table_to_json_array(data_table)
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

    def put(self, id, json_data):
        http_status_code = 500
        message = "Unknow"
        data = None
        try:
            status = json_data["status"]
        except:
            http_status_code = 400
            message = "Invalid status value."
            data = None
        sql = """update profile_agent set status = %s, last_update=unix_timestamp() where id=%s"""%(status, id)
        status, message, data_table = self.db.execute_non_query(sql)
        if status == 1:
            http_status_code = 400
            message = message
            data = None
        if status == 0:
            http_status_code = 202
            message = message
            data = data_table
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

class Snmp:
    def __init__(self):
        self.db = Database()

    def parse_profile_data_table_to_json_array(self, profile_list):
        agent = {}
        args = []
        for profile in profile_list:
            args.append({ 
                            'id'                     : profile[0] if profile[0] else None,
                            'name'                   : profile[1] if profile[1] else "",
                            'ip'                     : profile[2] if profile[2] else "",
                            'type'                   : profile[3] if profile[3] else "",
                            'monitor'                : profile[4] if profile[4] else 0,
                            'status'                 : profile[5] if profile[5] else 0,
                            'analyzer'               : profile[6] if profile[6] else 0,
                            'analyzer_status'        : profile[7] if profile[7] else 0,
                        })
        agent["profile_agent_snmp"] = args
        return agent        

    def get(self):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = """select pa.id,c.name,p.ip,p.type,pa.monitor,pa.status,pa.analyzer,pa.analyzer_status 
                from profile as p, agent as a, profile_agent as pa,channel as c 
                where a.ip='%s' and (pa.monitor=1 or pa.analyzer=1) and a.active=1 and p.channel_id=c.id and pa.profile_id=p.id and pa.agent_id=a.id 
                order by c.name"""%(ip)
        status, message, data_table = self.db.execute_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = self.parse_profile_data_table_to_json_array(profile_list = data_table)
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response
