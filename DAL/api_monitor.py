import requests # pip install requests
import json
from requests.exceptions import ConnectionError
from requests.auth import HTTPBasicAuth
from config import config

class ApiMonitor:
    def __init__(self, api_url):
        self.agent_url = api_url + "agent/"
        self.log_url = api_url + "log/"
        self.profile_agent_url = api_url + "profile_agent/"
        self.snmp_url = api_url + "profile_agent/snmp/" + config.IP

    def get(self, url):
        message = "Unknow"
        data = None
        status = 500
        try:
            rsp = requests.get(url, auth=HTTPBasicAuth(config.USER, config.PASSWD), timeout=5)
        except ConnectionError as e:
            message = str(e)
            data = None
            status = 500
            json_response = {"status": status, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        if rsp.status_code == 200:
            message = "OK"
            try:
                data = rsp.json()
                data = data['data']
            except:
                data = None
            status = rsp.status_code
        elif rsp.status_code == 502:
            message = "Check your proxy or web services"
            data =None
            status = rsp.status_code
        else:
            message = "Unknow"
            data = str(rsp.text)
            status = rsp.status_code
        json_response = {"status": status, "message": message, "data": data}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def put(self, url, json_data):
        message = "Unknow"
        data = None
        status = 500
        try:
            rsp = requests.put(url, json = json_data, auth=HTTPBasicAuth(config.USER, config.PASSWD), timeout=5)
        except ConnectionError as e:
            message = str(e)
            data = None
            status = 500
            json_response = {"status": status, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        if rsp.status_code == 202:
            message = "OK"
            try:
                data = rsp.json()
            except:
                data = None
            status = rsp.status_code
        elif rsp.status_code == 502:
            message = "Check your proxy or web services"
            data =None
            status = rsp.status_code
        elif rsp.status_code == 400:
            message = "Bad request"
            data = rsp.json()
            status = rsp.status_code
        else:
            message = "Unknow"
            data = str(rsp.text)
            status = rsp.status_code
        json_response = {"status": status, "message": message, "data": data}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

    def post(self, url, json_data):
        message = "Unknow"
        data = None
        status = 500
        try:
            rsp = requests.post(url, json = json_data, auth=HTTPBasicAuth(config.USER, config.PASSWD), timeout=5)
        except ConnectionError as e:
            message = str(e)
            data = None
            status = 500
            json_response = {"status": status, "message": message, "data": data}
            json_response = json.dumps(json_response)
            return json.loads(json_response)
        if rsp.status_code == 201:
            message = "OK"
            try:
                data = rsp.json()
            except:
                data = None
            status = rsp.status_code
        elif rsp.status_code == 502:
            message = "Check your proxy or web services"
            data =None
            status = rsp.status_code
        elif rsp.status_code == 400:
            message = "Bad request"
            try:
                data = rsp.json()
            except:
                data = None
            status = rsp.status_code
        else:
            message = "Unknow"
            data = str(rsp.text)
            status = rsp.status_code
        json_response = {"status": status, "message": message, "data": data}
        json_response = json.dumps(json_response)
        return json.loads(json_response)

