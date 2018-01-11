import requests # pip install requests
import json
from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
from config import config

class ApiMonitor:
    def __init__(self):
        self.agent_url = config.URL_AGENT
        self.log_url = config.URL_LOG
        self.profile_agent_url = config.URL_PROFILE_AGENT
        self.snmp_url = config.URL_SNMP

    def get(self, url):
        try:
            rsp = requests.get(url, auth=HTTPBasicAuth(config.USER, config.PASSWD), timeout=5)
        except ConnectionError as e:
            message = str(e)
            data = None
            status = 500
            json_response = {"status": status, "message": message, "data": data}
            json_response = json.dumps(json_response)
            json_response = json.loads(json_response)
            return json_response
        if rsp.status_code == 200:
            message = "OK"
            data = rsp.json()
            json_response = {"status": rsp.status_code, "message": message,"data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        elif rsp.status_code == 502:
            message = "Check your proxy or web services"
            data =None
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        else:
            message = "Unknow"
            data = str(rsp.text)
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json.loads(json.loads(json_response)))

    def put(self, url, data):
        try:
            rsp = requests.put(url, json = data, auth=HTTPBasicAuth(config.USER, config.PASSWD), timeout=5)
        except ConnectionError as e:
            message = str(e)
            data = None
            status = 500
            json_response = json.dumps(json_response)
            json_response = json.loads(json_response)
            return json_response
        if rsp.status_code == 202:
            message = "OK"
            try:
                data = rsp.json()
            except Exception as e:
                data = None
            json_response = {"status": rsp.status_code, "message": message,"data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        elif rsp.status_code == 502:
            message = "Check your proxy or web services"
            data =None
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        elif rsp.status_code == 400:
            message = "Bad request"
            data = rsp.json()
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        else:
            message = "Unknow"
            data = str(rsp.text)
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)

    def post(self, url, data):
        try:
            rsp = requests.post(url, json = data, auth=HTTPBasicAuth(config.USER, config.PASSWD), timeout=5)
        except ConnectionError as e:
            message = str(e)
            data = None
            status = 500
            json_response = json.dumps(json_response)
            json_response = json.loads(json_response)
            return json_response
        if rsp.status_code == 201:
            message = "OK"
            try:
                data = rsp.json()
            except Exception as e:
                data = None
            json_response = {"status": rsp.status_code, "message": message,"data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        elif rsp.status_code == 502:
            message = "Check your proxy or web services"
            data =None
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        elif rsp.status_code == 400:
            message = "Bad request"
            data = rsp.json()
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        else:
            message = "Unknow"
            data = str(rsp.text)
            json_response = {"status": rsp.status_code, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)

