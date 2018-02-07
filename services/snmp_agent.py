#!/usr/bin/python
import os
import logging
from config.config import SYSTEM
from utils import DateTime
from BLL.profile import Snmp as SnmpBLL
from utils.file import Snmp as LocalSnmp

class Snmp(object):
    """docstring for Snmp"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def execute_command(self, cmd):
        """
        Execute bash shell command
        """
        os.system(cmd)

    def write_null(self):
        self.execute_command("cat /dev/null > /monitor/snmp/agent/channel_name")
        self.execute_command("cat /dev/null > /monitor/snmp/agent/channel_status")
        self.execute_command("cat /dev/null > /monitor/snmp/agent/channel_profile")
        self.execute_command("cat /dev/null > /monitor/snmp/analyzer/channel_name")
        self.execute_command("cat /dev/null > /monitor/snmp/analyzer/channel_status")
        self.execute_command("cat /dev/null > /monitor/snmp/analyzer/channel_profile")

    def get_data(self):
        """
        get snmp API
        """
        snmpbll = SnmpBLL()
        data = snmpbll.get()
        if data['status'] == 200:
            return data['data']
        else:
            print data['message']
            self.logger.error(data['message'])
            exit(1)

    def create_snmp(self):
        profile_list = self.get_data()
        if not profile_list:
            print "Snmp data empty!"
            self.logger.warning("Snmp data empty")
            return 1
        """
        Refesh snmp file
        """
        self.write_null()
        """
        Make SNMP content
        """
        for profile in profile_list:
            #Agent_IPTV_Status
            if profile['monitor'] == 1:
                cmd="echo '%s-%s' >> /monitor/snmp/agent/channel_name"%(profile['name'],profile['type'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/agent/channel_profile"%(profile['ip'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/agent/channel_status"%(profile['status'])
                self.execute_command(cmd)
            #Agent_IPTV_Analyzer
            if profile['analyzer'] == 1:
                cmd="echo '%s-%s' >> /monitor/snmp/analyzer/channel_name"%(profile['name'],profile['type'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/analyzer/channel_profile"%(profile['ip'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/analyzer/channel_status"%(profile['analyzer_status'])
                self.execute_command(cmd)
        self.logger.warning("Snmp update --> OK")
        return 0

    def create_snmp_video_check(self):
        profile_list = self.get_data()
        if not profile_list:
            print "Snmp data empty!"
            self.logger.warning("Snmp data empty")
            return 1
        """
        Refesh snmp file
        """
        self.write_null()
        """
        Make SNMP content
        """
        for profile in profile_list:
            #Agent_IPTV_Status
            if profile['monitor'] == 1:
                if profile['status'] == 1 and profile['video_status'] != 1:
                    status = 2
                else:
                    status = profile['status']
                cmd="echo '%s-%s' >> /monitor/snmp/agent/channel_name"%(profile['name'],profile['type'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/agent/channel_profile"%(profile['ip'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/agent/channel_status"%(status)
                self.execute_command(cmd)
            #Agent_IPTV_Analyzer
            if profile['analyzer'] == 1:
                cmd="echo '%s-%s' >> /monitor/snmp/analyzer/channel_name"%(profile['name'],profile['type'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/analyzer/channel_profile"%(profile['ip'])
                self.execute_command(cmd)
                cmd="echo '%s' >> /monitor/snmp/analyzer/channel_status"%(profile['analyzer_status'])
                self.execute_command(cmd)
        self.logger.warning("Snmp update --> OK")
        return 0

    def create_snmp_at_broadcast_time(self):
        if SYSTEM["monitor"]["BLACK_SCREEN"] and SYSTEM["monitor"]["SOURCE"]:
            return self.create_snmp_video_check()
        elif not SYSTEM["monitor"]["BLACK_SCREEN"] and SYSTEM["monitor"]["SOURCE"]:
            return self.create_snmp()

    def create_snmp_at_broadcast_timeout(self):
        if SYSTEM["monitor"]["BLACK_SCREEN"] and SYSTEM["monitor"]["SOURCE"]:
            return self.create_snmp()
        elif not SYSTEM["monitor"]["BLACK_SCREEN"] and SYSTEM["monitor"]["SOURCE"]:
            return self.create_snmp()

    def set(self):
        date_time = DateTime()
        now = date_time.get_now()
        HH = date_time.get_hour(now)
        if HH > SYSTEM["broadcast_time"]["FROM"] and HH < SYSTEM["broadcast_time"]["TO"]:
            self.create_snmp_at_broadcast_time()
        else:
            self.create_snmp_at_broadcast_timeout()

class AgentSnmp(object):
    def __init__(self, profile = None, name = None, status = None):
        self.logger = logging.getLogger(__name__)
        self.profile = profile
        self.name = name
        self.status = status

    def get_line_posision(self):
        snmp = LocalSnmp()
        profile_list = snmp.read_profile()
        count = 0
        for line in profile_list.split('\n'):
            line = line.strip()
            count += 1
            if line == self.profile:
                break
        return count

    def update_profile(self, posision = None):
        snmp = LocalSnmp()
        channel_list = snmp.read_profile()
        new_channel_list = ""
        count = 0
        for line in channel_list.split('\n'):
            line = line.strip()
            count += 1
            if count != posision and line:
                new_channel_list = new_channel_list + line + "\n"
        new_channel_list = new_channel_list + self.profile
        return snmp.update_profile(new_channel_list)

    def update_status(self, posision = None):
        snmp = LocalSnmp()
        status_list = snmp.read_status()
        new_status_list = ""
        count = 0
        for line in status_list.split('\n'):
            line = line.strip()
            count += 1
            if count != posision and line:
                new_status_list = new_status_list + line + "\n"
        new_status_list = new_status_list + str(self.status)
        return snmp.update_status(new_status_list)

    def update_name(self, posision = None):
        snmp = LocalSnmp()
        name_list = snmp.read_name()
        new_name_list = ""
        count = 0
        for line in name_list.split('\n'):
            line = line.strip()
            count += 1
            if count != posision and line:
                new_name_list = new_name_list + line + "\n"
        new_name_list = new_name_list + self.name
        return snmp.update_name(new_name_list)

    def set(self):
        posision = self.get_line_posision()
        self.update_profile(posision)
        self.update_status(posision)
        self.update_name(posision)
