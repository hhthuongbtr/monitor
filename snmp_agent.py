#!/usr/bin/python
import os
from BLL.profile import Snmp as SnmpBLL

class Snmp:
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
        print data
        if data['status'] == 200:
            return data['data']
        else:
            print data['message']
            exit(1)

    def create_snmp_file(self):
        profile_list = self.get_data()
        if not profile_list:
            print "Snmp data empty!"
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
        return 0

if __name__ == "__main__":
    snmp = Snmp()
    snmp.create_snmp_file()

