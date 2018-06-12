import json
from config.config import SYSTEM
from database_monitor import Database

class Profile:
    def __init__(self, database):
        self.db = Database(database)
        
    def parse_profile_data_table_to_array(self, profile_list):
        args = []
        for profile in profile_list:
            args.append({ 
                            'id'            : profile[0] if profile[0] else None,
                            'ip'            : profile[2] if profile[2] else "",
                            'protocol'      : profile[3] if profile[3] else 'udp',
                            'status'        : profile[4] if profile[4] else 0,
                            'agent'         : profile[5] if profile[5] else "",
                            'thread'        : profile[6] if profile[6] else 10,
                            'name'          : profile[7] if profile[7] else "",
                            'type'          : profile[8] if profile[8] else None
                        })
        return args

    def get(self):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = """select pa.id, pa.last_update, p.ip, p.protocol, pa.status, a.name as agent, a.thread, c.name, p.type
                from profile as p, agent as a, profile_agent as pa,channel as c 
                where a.ip='%s' and a.active=1 and pa.monitor=1 and p.channel_id=c.id and pa.profile_id=p.id and pa.agent_id=a.id 
                order by pa.last_update desc"""%(SYSTEM["HOST"])
        status, message, data_table = self.db.execute_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = self.parse_profile_data_table_to_array(data_table)
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

    def get_by_ip_multicast(self, source):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = """select pa.id, p.ip, p.protocol, pa.status, a.name as agent, a.thread, c.name, p.type
            from profile as p, agent as a, profile_agent as pa,channel as c 
            where p.ip LIKE '%s:%%' and a.ip='%s' and a.active=1 and pa.monitor=1 and p.channel_id=c.id and pa.profile_id=p.id and pa.agent_id=a.id"""%(source,(SYSTEM["HOST"]))
        status, message, data_table = self.db.execute_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = self.parse_profile_data_table_to_array(data_table)
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

    def convert_profile_agent_check_video_list_to_array(self, data_table):
        args = []
        for profile_agent in data_table:
            args.append({ 
                            "id"                : profile_agent[0] if profile_agent[0] else None,
                            "ip"                : profile_agent[1] if profile_agent[1] else "",
                            "protocol"          : profile_agent[2] if profile_agent[2] else "udp",
                            "status"            : profile_agent[3] if profile_agent[3] else 0,
                            "thread"            : profile_agent[4] if profile_agent[4] else 10,
                            "name"              : profile_agent[5] if profile_agent[5] else "Unknow",
                            "agent"             : profile_agent[6] if profile_agent[6] else "Unknow",
                            "type"              : profile_agent[7] if profile_agent[7] else "",
                            "video_status"      : profile_agent[8] if profile_agent[8] else 0

                        })
        return args

    def get_video_check_list(self):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = """select pa.id, p.ip, p.protocol, pa.status, a.thread, c.name, a.name as agent_name, p.type, pa.video 
            from profile as p, agent as a, profile_agent as pa, channel as c 
            where a.ip = '%s' and a.active = 1 and pa.monitor = 1 and (pa.status = 1 or pa.video != 1) and pa.profile_id = p.id and pa.agent_id = a.id and p.channel_id = c.id"""%(SYSTEM["HOST"])
        status, message, data_table = self.db.execute_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = self.convert_profile_agent_check_video_list_to_array(data_table)
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response

    def put(self, id, json_data):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = ""
        if "status" in json_data:
            try:
                status = json_data["status"]
                sql = """update profile_agent set status = %s, last_update=unix_timestamp() where id=%s"""%(status, id)
            except:
                http_status_code = 400
                message = "Invalid status value."
                data = None
                json_response = {"status": http_status_code, "message": message, "data": data}
                json_response = json.dumps(json_response)
                json_response = json.loads(json_response)
                return json_response
        elif ("video" in json_data):
            try:
                video = json_data["video"]
                sql = """update profile_agent set video = %s, last_update=unix_timestamp() where id=%s"""%(video, id)
            except:
                http_status_code = 400
                message = "Invalid video value."
                data = None
                json_response = {"video": http_status_code, "message": message, "data": data}
                json_response = json.dumps(json_response)
                json_response = json.loads(json_response)
                return json_response
        if sql:
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
    def __init__(self, database):
        self.db = Database(database)

    def parse_profile_data_table_to_array(self, profile_list):
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
                            "video_status"           : profile[8] if profile[8] else 0
                        })
        return args        

    def get(self):
        http_status_code = 500
        message = "Unknow"
        data = None
        sql = """select pa.id,c.name,p.ip,p.type,pa.monitor,pa.status,pa.analyzer,pa.analyzer_status, pa.video 
                from profile as p, agent as a, profile_agent as pa,channel as c 
                where a.ip='%s' and (pa.monitor=1 or pa.analyzer=1) and a.active=1 and p.channel_id=c.id and pa.profile_id=p.id and pa.agent_id=a.id 
                order by c.name"""%(SYSTEM["HOST"])
        status, message, data_table = self.db.execute_query(sql)
        if status == 1:
            http_status_code = 500
            message = message
            data = None
        if status == 0:
            http_status_code = 200
            message = message
            data = self.parse_profile_data_table_to_array(profile_list = data_table)
        json_response = {"status": http_status_code, "message": message, "data": data}
        json_response = json.dumps(json_response)
        json_response = json.loads(json_response)
        return json_response
