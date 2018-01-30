#!/usr/bin/python
import os
import logging
from config import config
from utils import DateTime
from BLL.profile import Snmp as SnmpBLL

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
        if config.BLACK_SCREEN_MONITOR and config.SOURCE_MONITOR:
            return self.create_snmp_video_check()
        elif not config.BLACK_SCREEN_MONITOR and config.SOURCE_MONITOR:
            return self.create_snmp()

    def create_snmp_at_broadcast_timeout(self):
        if config.BLACK_SCREEN_MONITOR and config.SOURCE_MONITOR:
            return self.create_snmp()
        elif not config.BLACK_SCREEN_MONITOR and config.SOURCE_MONITOR:
            return self.create_snmp()

    def set(self):
        date_time = DateTime()
        now = date_time.get_now()
        HH = date_time.get_hour(now)
        if HH > config.BROADCAST_TIME_FROM and HH < config.BROADCAST_TIME_TO:
            self.create_snmp_at_broadcast_time()
        else:
            self.create_snmp_at_broadcast_timeout()

