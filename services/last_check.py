import json
import time
import logging
import threading
from utils.file import File
from utils import Ffmpeg
from utils import DateTime
from BLL.log import Log as LogBLL
from config.config import SYSTEM
from BLL.profile import Profile as ProfileBLL
from snmp_agent import Snmp

class LastCheck(object):
    """docstring for LastCheck"""
    def __init__(self):
        self.logger = logging.getLogger(__name__)


    def check_source(self, source, last_status, id, agent, name, type):
        """
        Get status of profile, if stastus not change then update check equal 1.      
        Ffmpeg: Use Ffprobe to check stastus profile (source) and return flag 
        0 is down
        1 is up
        2 is video error
        3 is audio eror 
        """
        ffmpeg = Ffmpeg()
        check = ffmpeg.check_source(source)
        # print "%s : %s"%(check, last_status)
        self.logger.debug("Curent :%s <> Last: %s, %s %s %s"%(check, last_status, source, name, type))
        if check != last_status:
            date_time = DateTime()
            opdate = date_time.get_now()
            time.sleep(SYSTEM["BREAK_TIME"])
            self.logger.debug("Recheck : %s %s %s"%(source, name, type))
            recheck = ffmpeg.check_source(source)
            if recheck == check:
                status = {0: "DOWN       ", 1: "UP         ", 2: "VIDEO ERROR", 3: "AUDIO ERROR"} [check]
                """
                Update status and write log
                """
                child_thread_list = []
                profile = ProfileBLL()
                profile_data = {"status": check, "agent": agent, "ip": SYSTEM["HOST"]}
                child_thread = threading.Thread(target=profile.put, args=(id, profile_data,))
                child_thread.start()
                child_thread_list.append(child_thread)
                """Append log"""
                channel = """%s %s"""%(name, type)
                while len(channel) < 22:
                    channel += " "
                while len(source) < 27:
                    source += " "
                ip_config = SYSTEM["HOST"]
                while len(ip_config) < 16:
                    ip_config += " "
                message = """%s (ip:%s) %s in host: %s (%s)""" % (channel, source, status, ip_config, agent)
                cldate = date_time.get_now()
                rslog = {
                         "sev"        : "Critical",
                         "jname"      : name,
                         "type"       : type,
                         "res"        : source,
                         "desc"       : status,
                         "cat"        : "Communication",
                         "host"       : agent,
                         "opdate"     : opdate,
                         "cldate"     : cldate
                     }
                self.logger.critical(json.dumps(rslog))
                log_data = {"host": source, "tag": "status", "msg": message}
                log = LogBLL()
                child_thread = threading.Thread(target=log.post, args=(log_data,))
                child_thread.start()
                child_thread_list.append(child_thread)
                """Update local snmp IPTV"""
                if "origin" or "4500" in agent:
                    self.logger.debug("%s is core probe"%(agent))
                    time.sleep(2)
                    snmp = Snmp()
                    child_thread = threading.Thread(target=snmp.set)
                    child_thread.start()
                    child_thread_list.append(child_thread)

                """
                Wait for update database complete
                """
                for child_thread in child_thread_list:
                    child_thread.join()
                return 1
        return 0

    def check(self):
        if not SYSTEM["monitor"]["SOURCE"]:
            message = "Black screen monitor is disable, check your config!"
            self.logger.error(message)
            print message
            time.sleep(60)
            exit(0)
        ancestor_thread_list = []
        file = File()
        profile_list = file.get_check_list()
        profile_list = profile_list[0:len(profile_list)-1]
        if(profile_list):
            for line in profile_list.split('\n'):
                self.logger.debug("Last Check : %s"%(line))
                profile = json.loads(line)
                while threading.activeCount() > profile['thread']:
                    time.sleep(1)
                t = threading.Thread(target=self.check_source,args=(profile['source'],
                    profile['status'],
                    profile['pa_id'],
                    profile['agent'],
                    profile['name'],
                    profile['type'],
                    )
                )
                t.start()
            #time.sleep(30)
                ancestor_thread_list.append(t)
        for ancestor_thread in ancestor_thread_list:
            ancestor_thread.join()
        time.sleep(5)

