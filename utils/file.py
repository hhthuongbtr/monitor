import os
import time
import json
import logging
import subprocess
from subprocess import call
from config import SUPERVISORD

def is_json(text):
    rt = False
    try:
        json.loads(text)
        rt = True
    except:
        pass
    return rt

class File:
    def __init__(self):
        self.filedir= "/tmp/checkdata.tmp"
        self.inprocess="/tmp/inprocess.tmp"
        if not os.path.exists(self.filedir):
            command="echo '\n' >"+self.filedir
            os.system(command)
        if not os.path.exists(self.inprocess):
            command="echo '\n' >"+self.inprocess
            os.system(command)
        self.logger = logging.getLogger("utils")

    def read(self, filename):
        lines = None
        try:
            f = open(filename, 'r')
            lines=f.read()
            f.close()
        except Exception as e:
            self.logger.error("%s"%(str(e)))
        return lines

    def write(self, dir, text):
        try:
            f = open(dir, 'w')
            f.write(text)
            f.close()
        except Exception as e:
            self.logger.error("%s"%(str(e)))
            return 1
        return 0

    def delete(self, filename):
        self.logger.debug("File.delete: %s"%(filename))
        cmnd = ['/bin/rm', '-rf', filename]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

    def get_check_list(self):
        #Read file checkdata.tmp
        lines = self.read(self.filedir)
        #Clear checkdata.tmp after read
        command="cat /dev/null > "+self.filedir
        os.system(command)
        #clear all and write data to inprocess file
        command="cat /dev/null > "+self.inprocess
        os.system(command)
        f = open(self.inprocess, 'a')
        f.write(lines)
        f.close()
        #return data
        return lines

    def append_to_check_list(self, text):
        data_rows = self.read(self.filedir)
        fips = open(self.inprocess, 'r')
        data_ips = fips.read()
        fips.close()
        if (text not in data_rows) and (text not in data_ips):
            f = open(self.filedir, 'a')
            f.write(text+"\n")
            f.close()
            return 0
        else:
            print "replicate"
            return 1

class Snmp:
    def __init__(self):
        self.agent_channel_status = "/monitor/snmp/agent/channel_status"
        self.agent_channel_name = "/monitor/snmp/agent/channel_name"
        self.agent_channel_profile = "/monitor/snmp/agent/channel_profile"
        self.analyzer_channel_status = "/monitor/snmp/analyzer/channel_status"
        self.analyzer_channel_name = "/monitor/snmp/analyzer/channel_name"
        self.analyzer_channel_profile = "/monitor/snmp/analyzer/channel_profile"

    def read_profile(self, file_path = None):
        file_path = self.channel_profile
        with open(file_path, "r") as text_file:
            return text_file.read()

    def read_status(self, file_path = None):
        file_path = self.channel_status
        with open(file_path, "r") as text_file:
            return text_file.read()

    def read_name(self, file_path = None):
        file_path = self.channel_name
        with open(file_path, "r") as text_file:
            return text_file.read()

    def update_agent_profile(self, text = None):
        f = open(self.agent_channel_profile, 'w')
        f.write(text)
        f.close()
        return 0

    def update_agent_status(self, text = None):
        f = open(self.agent_channel_status, 'w')
        f.write(text)
        f.close()
        return 0

    def update_agent_name(self, text = None):
        f = open(self.agent_channel_name, 'w')
        f.write(text)
        f.close()
        return 0

    def update_analyzer_profile(self, text = None):
        f = open(self.analyzer_channel_profile, 'w')
        f.write(text)
        f.close()
        return 0

    def update_analyzer_status(self, text = None):
        f = open(self.analyzer_channel_status, 'w')
        f.write(text)
        f.close()
        return 0

    def update_analyzer_name(self, text = None):
        f = open(self.analyzer_channel_name, 'w')
        f.write(text)
        f.close()
        return 0

class SupervisordFile:
    def __init__(self):
        pass

    def read(self, filename):
        f = open(SUPERVISORD["CONF_DIR"] + '/' + fileName, 'r')
        lines=f.read()
        f.close()
        return lines

    def write(self, dir, text):
        f = open(dir, 'w')
        f.write(text)
        f.close()

    def read_template(self):
        f = open(SUPERVISORD["CONF_TEMPLATE_DIR"], 'r')
        lines=f.read()
        f.close()
        return lines

    def write_conf_file(self, dir, text):
        f = open(dir, 'w')
        f.write(text)
        f.close()

    def delete(self, filename):
        cmnd = ['/bin/rm', '-rf', SUPERVISORD["CONF_DIR"] + '/' + fileName]
        p = subprocess.call(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)

