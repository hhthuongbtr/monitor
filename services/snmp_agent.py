import os
import logging
from config.config import SYSTEM
from utils import DateTime
from BLL.profile import Snmp as SnmpBLL
from utils.file import Snmp as FileSnmp

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
            self.logger.info("Snmp data empty")
            return 1
        """
        Refesh snmp file
        """
        self.write_null()
        """
        Make SNMP content
        """
        agent_channel_name = ""
        agent_channel_profile = ""
        agent_channel_status = ""
        analyzer_channel_name = ""
        analyzer_channel_profile = ""
        analyzer_channel_status = ""
        for profile in profile_list:
            #Agent_IPTV_Status
            if profile['monitor'] == 1:
                agent_channel_name += "%s-%s"%(profile['name'],profile['type']) + "\n"
                agent_channel_profile += "%s"%(profile['ip']) + "\n"
                agent_channel_status += "%s"%(profile['status']) + "\n"
            #Agent_IPTV_Analyzer
            if profile['analyzer'] == 1:
                analyzer_channel_name += "%s-%s"%(profile['name'],profile['type']) + "\n"
                analyzer_channel_profile += "%s"%(profile['ip']) + "\n"
                analyzer_channel_status += "%s"%(profile['analyzer_status']) + "\n"
        snmp = FileSnmp()
        snmp.update_agent_name(agent_channel_name)
        snmp.update_agent_profile(agent_channel_profile)
        snmp.update_agent_status(agent_channel_status)
        snmp.update_analyzer_name(analyzer_channel_name)
        snmp.update_analyzer_profile(analyzer_channel_profile)
        snmp.update_analyzer_status(analyzer_channel_status)
        self.logger.info("Snmp update --> OK")
        return 0

    def create_snmp_video_check(self):
        profile_list = self.get_data()
        if not profile_list:
            print "Snmp data empty!"
            self.logger.info("Snmp data empty")
            return 1
        """
        Refesh snmp file
        """
        self.write_null()
        """
        Make SNMP content
        """
        agent_channel_name = ""
        agent_channel_profile = ""
        agent_channel_status = ""
        analyzer_channel_name = ""
        analyzer_channel_profile = ""
        analyzer_channel_status = ""
        for profile in profile_list:
            #Agent_IPTV_Status
            if profile['monitor'] == 1:
                if profile['status'] == 1 and profile['video_status'] != 1:
                    status = 2
                else:
                    status = profile['status']
                agent_channel_name += "%s-%s"%(profile['name'],profile['type']) + "\n"
                agent_channel_profile += "%s"%(profile['ip']) + "\n"
                agent_channel_status += "%s"%(status) + "\n"
            #Agent_IPTV_Analyzer
            if profile['analyzer'] == 1:
                analyzer_channel_name += "%s-%s"%(profile['name'],profile['type']) + "\n"
                analyzer_channel_profile += "%s"%(profile['ip']) + "\n"
                analyzer_channel_status += "%s"%(profile['analyzer_status']) + "\n"
        snmp = FileSnmp()
        snmp.update_agent_name(agent_channel_name)
        snmp.update_agent_profile(agent_channel_profile)
        snmp.update_agent_status(agent_channel_status)
        snmp.update_analyzer_name(analyzer_channel_name)
        snmp.update_analyzer_profile(analyzer_channel_profile)
        snmp.update_analyzer_status(analyzer_channel_status)
        self.logger.info("Snmp update --> OK")
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
        self.logger.debug("FileSnmp: %s %s %s"%(profile, str(status), name))
        self.profile = profile
        self.name = name
        self.status = status

    def get_line_posision(self):
        snmp = FileSnmp()
        profile_list = snmp.read_profile()
        count = 0
        for line in profile_list.split('\n'):
            line = line.strip()
            count += 1
            self.logger.debug("%s ? %s"%(self.profile, line))
            if line == self.profile:
                self.logger.debug("Break")
                break
        self.logger.debug("Position: %d len: %d -->  %s %s %s"%(count, len(profile_list), self.profile, str(self.status), self.name))
        return count

    def update_profile(self, posision = None):
        snmp = FileSnmp()
        channel_list = snmp.read_profile()
        new_channel_list = ""
        count = 0
        for line in channel_list.split('\n'):
            line = line.strip()
            count += 1
            if count != posision:
                self.logger.debug("%d?%d"%(posision, count))
                new_channel_list = new_channel_list + line + "\n"
        new_channel_list = new_channel_list + self.profile
        self.logger.debug("Upadte profile: %s --> OK"%(self.profile))
        return snmp.update_agent_profile(new_channel_list)

    def update_status(self, posision = None):
        snmp = FileSnmp()
        status_list = snmp.read_status()
        new_status_list = ""
        count = 0
        for line in status_list.split('\n'):
            line = line.strip()
            count += 1
            if count != posision:
                new_status_list = new_status_list + line + "\n"
        new_status_list = new_status_list + str(self.status)
        self.logger.debug("Upadte status: %s --> OK"%(str(self.status)))
        return snmp.update_agent_status(new_status_list)

    def update_name(self, posision = None):
        snmp = FileSnmp()
        name_list = snmp.read_name()
        new_name_list = ""
        count = 0
        for line in name_list.split('\n'):
            line = line.strip()
            count += 1
            if count != posision:
                new_name_list = new_name_list + line + "\n"
        new_name_list = new_name_list + self.name
        self.logger.debug("Upadte name: %s --> OK"%(self.name))
        return snmp.update_agent_name(new_name_list)

    def set(self):
        posision = self.get_line_posision()
        self.update_profile(posision)
        self.update_status(posision)
        self.update_name(posision)
        self.logger.debug("Move to down: %s %s %s --> OK"%(self.profile, str(self.status), self.name))


